from django.template import Library

register = Library()

def query_media_prefix():
    """
    Returns the string contained in the setting query_MEDIA_PREFIX.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    try:
       return settings.QUERY_MEDIA_PREFIX
    except:
       return settings.ADMIN_MEDIA_PREFIX
query_media_prefix = register.simple_tag(query_media_prefix)
