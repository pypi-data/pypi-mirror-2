from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail, create_update
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from djangopypi.decorators import user_owns_package, user_maintains_package
from djangopypi.models import Package, Release, Distribution
from djangopypi.forms import ReleaseForm



def index(request, **kwargs):
    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('queryset',Release.objects.filter(hidden=False))
    return list_detail.object_list(request, **kwargs)

def details(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)
    
    if not release:
        return Http404()
    
    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('template_name','djangopypi/release_detail.html')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    
    kwargs['extra_context'][kwargs['template_object_name']] = release
        
    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])

def doap(request, package, version, **kwargs):
    kwargs.setdefault('template_name','djangopypi/release_doap.xml')
    kwargs.setdefault('mimetype', 'text/xml')
    return details(request, package, version, **kwargs)

@user_maintains_package()
def manage(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)
    
    if not release:
        return Http404()
    
    kwargs['object_id'] = release.pk
    
    kwargs.setdefault('form_class', ReleaseForm)
    kwargs.setdefault('template_name', 'djangopypi/release_manage.html')
    kwargs.setdefault('template_object_name', 'release')
    
    return create_update.update_object(request, **kwargs)

@user_maintains_package()
def manage_metadata(request, package, version, **kwargs):
    kwargs.setdefault('template_name', 'djangopypi/release_manage.html')
    kwargs.setdefault('template_object_name', 'release')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    
    release = get_object_or_404(Package, name=package).get_release(version)
    
    if not release:
        return Http404()
    
    if not release.metadata_version in settings.DJANGOPYPI_METADATA_FORMS:
        #TODO: Need to change this to a more meaningful error
        return Http404()
    
    kwargs['extra_context'][kwargs['template_object_name']] = release
    
    form_class = settings.DJANGOPYPI_METADATA_FORMS.get(release.metadata_version)
    
    initial = {}
    multivalue = ('classifier',)
    
    for key, values in release.package_info.iterlists():
        if key in multivalue:
            initial[key] = values
        else:
            initial[key] = '\n'.join(values)
    
    if request.method == 'POST':
        form = form_class(data=request.POST, initial=initial)
        
        if form.is_valid():
            for key, value in form.cleaned_data.iteritems():
                if isinstance(value, basestring):
                    release.package_info[key] = value
                elif hasattr(value, '__iter__'):
                    release.package_info.setlist(key, list(value))
            
            release.save()
            print str(release.package_info)
            return create_update.redirect(kwargs.get('post_save_redirect',None),
                                          release)
    else:
        form = form_class(initial=initial)
    
    kwargs['extra_context']['form'] = form
    
    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])

@user_maintains_package()
def manage_files(request, package, version, **kwargs):
    package = get_object_or_404(Package, name=package)
    try:
        release = package.releases.get(version=version)
    except Release.DoesNotExist:
        return Http404()
    
    kwargs.setdefault('formset_factory_kwargs',{})
    kwargs['formset_factory_kwargs'].setdefault('fields', ('comment',))
    kwargs['formset_factory_kwargs']['extra'] = 0
    
    kwargs.setdefault('formset_factory', inlineformset_factory(Release, Distribution, **kwargs['formset_factory_kwargs']))
    kwargs.setdefault('template_name', 'djangopypi/release_manage_files.html')
    kwargs.setdefault('template_object_name', 'release')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    kwargs['extra_context'][kwargs['template_object_name']] = release
    kwargs.setdefault('formset_kwargs',{})
    kwargs['formset_kwargs']['instance'] = release
    
    if request.method == 'POST':
        formset = kwargs['formset_factory'](data=request.POST,
                                            files=request.FILES,
                                            **kwargs['formset_kwargs'])
        if formset.is_valid():
            formset.save()
            return create_update.redirect(kwargs.get('post_save_redirect',None),
                                          release)
    
    formset = kwargs['formset_factory'](**kwargs['formset_kwargs'])
    
    kwargs['extra_context']['formset'] = formset
    
    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])