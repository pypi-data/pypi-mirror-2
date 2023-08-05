# -*- coding: utf-8 -*-
import sys
from django.conf import settings

def autodiscover_handlers():
    """
    Register signal handlers from each addon.
    """
    for addon in settings.ADDONS:
        fullname = "%s.%s.handlers" % (settings.ADDONS_PREFIX, addon)
        try:
            __import__(fullname)
        except ImportError, err:
            if str(err) != "No module named handlers":
                raise err

        if fullname in sys.modules:
            handlers = sys.modules[fullname]
            handlers.connect()

def autodiscover_notifications():
    """
    Register notifications from each addon.
    TODO: Implement this with signals. Requires changes in django-notifications upstream.
    """
    for addon in settings.ADDONS:
        fullname = "%s.%s.notifications" % (settings.ADDONS_PREFIX, addon)
        try:
            __import__(fullname)
        except ImportError:
            pass

def autodiscover():
    autodiscover_notifications()
    autodiscover_handlers()
