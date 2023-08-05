from django.conf import settings
from django.http import HttpResponseNotAllowed

from djangopypi.models import Package, Release
from djangopypi.http import HttpResponseNotImplemented
from djangopypi.http import parse_distutils_request



def root(request, fallback_view=None, **kwargs):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """
    
    if request.method != 'POST':
        if fallback_view is None:
            fallback_view = settings.DJANGOPYPI_FALLBACK_VIEW
        return fallback_view(request, **kwargs)
    
    parse_distutils_request(request)
    action = request.POST.get(':action','')
    
    if not action in settings.DJANGOPYPI_ACTION_VIEWS:
        print 'unknown action: %s' % (action,)
        return HttpResponseNotAllowed(settings.DJANGOPYPI_ACTION_VIEW.keys())
    
    return settings.DJANGOPYPI_ACTION_VIEWS[action](request, **kwargs)
