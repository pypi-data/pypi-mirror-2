from os import path
import sys
from werkzeug import Request, ClosingIterator, run_simple, SharedDataMiddleware
from werkzeug.routing import Rule
from werkzeug.exceptions import HTTPException, NotFound
from jinja2 import Environment, FileSystemLoader
from buro.shared import local, local_manager
from buro.urls import url_map
from buro.responses import Response
from buro.errors import BuroError
from buro.utils import merge_dicts

class Configuration(dict):
    """Dict on steroids for the configuration. You can import your settings
    from a python file (:attr:`load_pyfile`) or from a python object
    (:attr:`load_object`). The configuration is automatically filled with the
    default settings, then Buro tries to load the ``settings.py`` from your
    project's root.
    
    Note: this class as been shamefully stolen from the source of the 
    `Flask <http://flask.pocoo.org/>`_ project.
    """
    
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})
        
    def load_pyfile(self, filename):
        """Load the configuration from a Python file. All the settings must be
        in uppercase.
        
        :param filename: the path to the Python file which must be loaded.
        
        Example::
        
            DEBUG = True
            TEMPLATES = "templates/"
        """
        d = type(sys)('config')
        d.__file__ = filename
        execfile(filename, d.__dict__)
        self.load_object(d)
        
    def load_object(self, obj):
        """Load the configuration from a Python object (dict).
        
        :param obj: the dict which must be loaded.
        
        Example::
        
            d = {'DEBUG':True, 'TEMPLATES': 'templates/'}
            app.configuration.load_object(d)
        """
        if isinstance(obj, basestring):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
                
    def __repr__(self):
        txt = 'Configuration:\n'
        for key, value in self.iteritems():
            txt += '\t%s => %s\n' % (key, value)
        return txt


        
class Buro(object):
    """The Buro object implements the whole WSGI application: this is the main
    object. It uses Werkzeug for the WSGI stuff and pure Python for the logic.
    
    You can create a simple Buro application quite easily::
    
        from buro import Buro, get_path
        app = Buro(get_path(__file__))
    """

    def __init__(self, root_path):
        # Store the root_path
        self.root_path = root_path
        
        # Define the settings path
        self.settings_path = path.join(root_path, 'settings.py')
        
        # Set up the configuration
        self.config = Configuration()
        
        # Load the default configuration
        self.config.load_pyfile(path.join(path.dirname(__file__), 'settings.py'))
        
        try: # Try to load the user-defined configuration
            self.config.load_pyfile(self.settings_path)
        except IOError:
            pass # No such file or directory
        
        # Expand the templates path if needed (thanks to Python's magical
        # powers).
        self.config['TEMPLATES'] = path.join(self.root_path,\
                                             self.config['TEMPLATES'])
        
        # Expand MEDIA_ROOT
        self.config['MEDIA_ROOT'] = path.join(self.root_path,\
                                              self.config['MEDIA_ROOT'])
        
        # TODO Factor the expand process
        
        # Init internal components
        local.application = self
        self.local_mapping = {}
        self.jinja_env = Environment(loader=FileSystemLoader(\
                                                    self.config['TEMPLATES']))
        
        # Set up the media service system
        # Note: this is a bad thing for production.
        self._dispatch = SharedDataMiddleware(self._dispatch, {
            self.config['MEDIA_URL']: self.config['MEDIA_ROOT']
        })
        
        url_map.add(Rule(path.join(self.config['MEDIA_URL'], '<file>'),
                         endpoint = 'static',
                         build_only = True))
        
        self.endpoints_handlers = {
            'template': self.template,
            'function': self.function,
            'markup': self.markup,
        }

        # Special Pages handlers
        self.special_handlers = {
            #'404': ('handler', kwargs),
        }
        
        print self.config

        
    def __call__(self, environ, start_response):
        return self._dispatch(environ, start_response)
    
    def _dispatch(self, environ, start_response):
        local.application = self
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            response = self._endpoint_manager(endpoint, request, values)
        except NotFound, e:
            stored_data = self.special_handlers.get('404', None)
            if stored_data == None:
                response = e
            else:
                handler = self.endpoints_handlers.get(stored_data[0], False)
                if not handler:
                    raise BuroError("No handler named %s" % data[0])
                response = handler(stored_data[1], request)
            response.status_code = 404
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),\
                                        [local_manager.cleanup])
    
    def _endpoint_manager(self, endpoint, request, values):
        data = self.local_mapping.get(endpoint)
        
        handler = self.endpoints_handlers.get(data[0], False)
        
        if not handler:
            raise BuroError("No handler named %s" % data[0])

        info = data[1]

        return handler(info, request, **values)
    
    def set_special_handler(self, **kwargs):
        """Set a handler for a special page. Special pages are returned when a
        non 200 HTTP status code is returned (so 404, 500...). For now, only
        404 is implemented.
        
        Example::
        
            def view(request):
                return Response('can haz cheezburger?')
            
            app.set_special_handler(name='404', handler='function', function=view)
        
        Now all your not found pages will print "can haz cheezburger?" instead
        of the 404 page of your web browser.
        """
        name = kwargs.get('name', False)
        if not name:
            raise BuroError('You must provide the name of the special handler.')
        
        handler = kwargs.get('handler', False)
        if not handler:
            raise BuroError("Your special handler doesn't have a handler")
        
        if not handler in self.endpoints_handlers:
            raise BuroError("%s is not a loaded handler." % handler)
            
        data = (handler, kwargs)

        self.special_handlers[name] = data
    
    def set_404(self):
        """Decorator to set the decorated function as the special handler for
        not found pages.
        
        Example::
        
            @app.set_404()
            def myfunction(request):
                return Response('This page does not exist you know?')
        """
        def decorate(f):
            kwargs = {'name':'404', 'function':f, 'handler':'function'}
            self.set_special_handler(**kwargs)
            return f
        return decorate
    
    def set_404_html(self, template, **infos):
        """Helper function to set a template as the special handler for not
        found pages.
        
        Example::
        
            app.set_404_html('404.html')
            
        Or with custom context::
        
            app.set_404_html('404.html', VERSION='4.2')
        """
        kwargs = {'name': '404', 'template':template, 'handler':'template'}
        final = kwargs
        final.update(infos)
        self.set_special_handler(**final)
    
    def set_404_markdown(self, **infos):
        """Helper function to set a markdown file as the special handler for
        not found pages.
        
        Example::
        
            app.set_404_markdown(template='context.html', file='data/404.md')
        """
        kwargs = {'name': '404', 'handler':'markup', 'markup': 'markdown'}
        final = kwargs
        final.update(infos)
        self.set_special_handler(**final)
    
    def function(self, info, request, **values):
        # Handle the request with a function
        return info['function'](request, **values)
    
    def template(self, info, request, **values):
        # Handle a request by rendering a template
        context = info.get('context', {})
        return self.render_template(info['template'], **context)
    
    def markup(self, info, request, **values):
        template = info.get('template', None)
        if template == None:
            raise BuroError("You need to provide the 'template' kwarg.")

        # TODO Move it to the global configuration, maybe with autodetection
        supported_markups = ['markdown',]
        markup = info.get('markup')
        
        if not markup in supported_markups:
            raise BuroError("%s is not a supported markup. Supported are:\
                             %s", (markup, supported_markups))

        file_name = info.get('file', False)
        string = info.get('string', False)
        content = ""

        if not file_name:
            if not string:
                raise BuroError("You must provide a file or string kwarg.")
            else:
                content = string
        else:
            full_path = path.join(self.root_path, file_name)
            f = open(full_path, 'r')
            content = f.read()
            f.close()
        
        if markup == 'markdown':
            import markdown
            plugins = []
            highlight = info.get('highlight', True)
            
            if highlight == True:
                force_lineos = info.get('force_lineos', False)
                if force_lineos == True:
                    plugins.append('codehilite(force_linenos=True)')
                else:
                    plugins.append('codehilite')
            
            html = markdown.markdown(content, plugins)
            context = info.get('context', {})
            
            
            return self.render_template(template, content=html, **context)
    
    def render_template(self, template, **context):
        """Render the given :attr:`template` file and put it in a 
        :attr:`~buro.Buro.Response` object.
        
        :param template: the template file name relative to the ``templates`` 
                         directory.
        
        """
        context = merge_dicts(self.config, context)
        return Response(self.jinja_env.get_template(template).render(**context))
    
    
    def url(self, url, **opts):
        """Decorator to publish a custom view (function).
        
        Publish a simple page::
        
            @app.url('/hello/')
            def foo(request):
                return application.render_template('bar.html')
        
        Publish a page with one argument::
        
            @application.url('/user/<name>/')
            def user(request, name):
                return application.render_template('profile.html', name=name)
        
        This is equivalent to :attr:`publish` with the ``function`` argument.
        """
        def decorate(f):
            url_map.add(Rule(url, endpoint=url))
            data = ['function', {'function': f}]
            self.local_mapping[url] = data
            return f
        return decorate
    
    def publish_html(self, **kwargs):
        """Publish a static HTML (with Jinja2 templating system). This is a
        shortcut for ``publish(handler='template')``.
        
        * :attr:`url` is the visible url.
        * :attr:`template` is the template name you want to render.
        
        Example::
        
            from buro import Buro, get_path
            app = Buro(get_path(__file__))
            app.publish_html(url="/", template="index.html")
        """
        data = kwargs
        data['handler'] = 'template'
        self.publish(**data)
    
    def publish_markdown(self, **kwargs):
        """Publish a markown file rendered in a template file (with Jinja2
        templating system). This is a shortcut for
        ``publish(handler='markup', markup='markdown')``.
        
        * :attr:`url` is the visible url.
        * :attr:`file` the markdown formatted file which will be rendered.
        * :attr:`string` the markdown string which will be rendered if not
          file is provided.
        * :attr:`template` is the template name you want to render.
        
        Example::
        
            from buro import Buro, get_path
            app = Buro(get_path(__file__))
            app.publish_markdown(url="/", file='blah.md' template="index.html")
            
        The handler adds a ``content`` variable to the template's context.
        """
        data = kwargs
        data['handler'] = 'markup'
        data['markup'] = 'markdown'
        self.publish(**data)
    
    
    def publish(self, **kwargs):
        """Put something visible on the website. You can basically add
        anything which returns a Werkzeug Response object. However some 
        shortcuts are built-in for you.
        
        Needed kwargs:
        
        * ``url`` is the visible url (``'/'``, ``'/license/'`` etc...)
        * ``handler`` is the name of a supported handler.
        
        Typical usages:
        
        * Publish some static HTML (parsed with Jinja2):
        
            * :attr:`template` is the template filename relative to the
              templates dir.
              
            Example::
            
                from buro import Buro, get_path
                app = Buro(get_path(__file__))
                app.publish(handler="template", url="/", template="index.html")
                
        * Expose a custom view (function):
        
            * :attr:`function` is the function you want tot expose.
            
            Example::
            
                from buro import Buro, get_path
                app = Buro(get_path(__file__))
                def bio(request):
                    return app.render_template('blah.html')
                app.publish(handler="function", url="/me/", function=bio)
                
            Note: is usage is equivalent to the :attr:`url` decorator.
        """
        publish_handler = kwargs.get('handler', False)
        if not publish_handler:
            raise BuroError("Your publish doesn't have a handler.")

        if not publish_handler in self.endpoints_handlers:
            raise BuroError("%s is not a loaded handler." % publish_handler)
                        
        data = [publish_handler, kwargs]
        
        self.local_mapping[kwargs['url']] = data
        url_map.add(Rule(kwargs['url'], endpoint=kwargs['url']))
    
    
    def run(self, host="127.0.0.1", port=8000, **options):
        """Start a local developement server. If :attr:`debug` is set, it will
        automatically reload when code changes and will print a debug page 
        with a complete trackback when an error triggers.
        
        :param host: hostname to listen on. ``'0.0.0.0'`` for al interfaces.
        :param port: the port to listen on.
        :param options: options to be passed to the Werkzeug run_simple method.
        """
        if 'debug' in options:
            self.config['DEBUG'] = options.pop('debug')
        options.setdefault('use_reloader', self.config['DEBUG'])
        options.setdefault('use_debugger', self.config['DEBUG'])
        return run_simple(host, port, self, **options)