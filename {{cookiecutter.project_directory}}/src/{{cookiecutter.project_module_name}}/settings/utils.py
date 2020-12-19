
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Callback for settings.DEBUG_TOOLBAR_CALLBACK['SHOW_TOOLBAR_CALLBACK']
def show_toolbar(request):
    """Prevent DjDT from appearing in Django-CMS admin page iframes"""
    path = request.get_full_path()

    if 'cms/' in path or 'admin/' in path:
        return False

    return True
