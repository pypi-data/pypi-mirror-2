from setuptools import setup


setup(
    name='Buro',
    version='0.1',
    url="http://buro.sourceinhabitants.com/",
    license='BSD',
    author='Thomas Pelletier',
    author_email='thomas@pelletier.im',
    description='A very simple Python-powered open-source web framework '
                'inspired by Flask, but following different design decisions',
    py_modules=['buro'],
    platforms='any',
    install_requires = [
    'Jinja2>=2.5',
    'Werkzeug>=0.6.2',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
    
)