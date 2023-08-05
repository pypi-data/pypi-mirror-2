
from urlparse import urlsplit
from os.path import split

from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404

####
# Helpers
####

def get_section_setting(section, key, default=None):
    """Get a setting from the settings file.

    section - The name of a variable holding a dict in settings.py. Usually all uppercase.
    key     - The key in the section that holds the value you're interested in.
    defautl - The value to return if section or key not found.
    """
    section_dict = get_setting(section, None)
    if isinstance(section_dict, dict):
        return section_dict.get(key, default)
    return default

def get_setting(key, default=None):
    return getattr(settings, key, default)

####
# Context processors
####

class BreadCrumb(object):
    def __init__(self, url, name, view):
        self.url = url
        self.name = name
        self.view = view

    def __repr__(self):
        return "BreadCrumb(url=%r, name=%r, view=%r)" % (self.url, self.name, self.view)

def _add_slash(path):
    return path + "/"

def _identity(path):
    return path

def _get_path_elements(path):
    append_slash = get_setting("APPEND_SLASH", True)
    if append_slash:
        finalize = _add_slash
    else:
        finalize = _identity
    parsed = urlsplit(path)
    current_path = parsed.path
    while current_path != "/":
        if current_path.endswith("/"):
            current_path, junk = split(current_path)
        next_path, current_name = split(current_path)
        yield finalize(current_path), current_name
        current_path = next_path
    yield finalize(current_path), "ROOT"

def add_breadcrumbs(request):
    """Add breadcrumbs to a request.

    Usage:
        Add "ibidem.django.util.add_breadcrumbs" to TEMPLATE_CONTEXT_PROCESSORS in your settings.py.
    """
    crumbs = list()
    home = get_section_setting("BREADCRUMBS", "home", "/")
    homename = get_section_setting("BREADCRUMBS", "homename", "Home")
    for url, name in _get_path_elements(request.get_full_path()):
        if url == home:
            name = homename
        try:
            view, args, kwargs = resolve(url)
        except Resolver404:
            continue
        crumbs.append(BreadCrumb(url, name, view))
    crumbs.reverse()
    if not get_section_setting("BREADCRUMBS", "include_current", False):
        crumbs = crumbs[:-1]
    if not get_section_setting("BREADCRUMBS", "include_home", True):
        crumbs = crumbs[1:]
    return {"crumbs": crumbs}
