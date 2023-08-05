from queries.helpers import ACTION_CHECKBOX_NAME
from queries.options import ModelQuery, InlineModelQuery, HORIZONTAL, VERTICAL
from queries.sites import QuerySite, site
from django.utils.importlib import import_module

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
LOADING = False

def autodiscover():
    """
    Auto-discover INSTALLED_APPS query.py modules and fail silently when
    not present. This forces an import on them to register any query bits they
    may want.
    """
    # Bail out if autodiscover didn't finish loading from a previous call so
    # that we avoid running autodiscover again when the URLconf is loaded by
    # the exception handler to resolve the handler500 view.  This prevents an
    # query.py module with errors from re-registering models and raising a
    # spurious AlreadyRegistered exception (see #8245).
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an query.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for query.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own query registration.
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's query.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its query.py doesn't exist
        try:
            imp.find_module('query', app_path)
        except ImportError:
            continue

        # Step 3: import the app's query file. If this has errors we want them
        # to bubble up.
        import_module("%s.query" % app)
    # autodiscover was successful, reset loading flag.
    LOADING = False
