def merge_dicts(source, dest):
    """Copy the content of the source dict to the dest dict."""
    for key, value in source.iteritems():
        dest[key] = value
    return dest