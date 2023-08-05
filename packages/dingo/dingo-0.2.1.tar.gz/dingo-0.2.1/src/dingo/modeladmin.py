import functools

from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects, model_ngettext, model_format_dict
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.functional import update_wrapper
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django import template
from django.shortcuts import render_to_response

import registry

def get_urls(self):
    """Return the URLs for the model admin, adding any model or 
    object views.

    Adapted from django.contrib.admin.options.ModelAdmin.get_urls"""

    from django.conf.urls.defaults import patterns, url
    import functools

    def wrap_dingo_view(view):
        
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(
                update_wrapper(functools.partial(view, self), view))(
                *args, **kwargs)

        return update_wrapper(wrapper, view)

    object_view_patterns = [
        url(r'^(.+)/%s/$' % a.__name__,
            wrap_dingo_view(a),
            name='%s_%s_%s' % (self.model._meta.app_label, 
                               self.model._meta.module_name, 
                               a.__name__))
        for a in registry.views(self.model, 'object')]
    
    model_view_patterns = [
        url(r'^%s/$' % a.__name__,
            wrap_dingo_view(a),
            name='%s_%s_%s' % (self.model._meta.app_label, 
                               self.model._meta.module_name, 
                               a.__name__))
        for a in registry.views(self.model, 'model')]

    urlpatterns = patterns('', 
                           *(model_view_patterns + 
                             object_view_patterns)) + \
                           super(self.__class__, self).get_urls()


    return urlpatterns

def change_view(self, request, object_id, extra_context=None):
    """View the change form for an object."""

    if extra_context is None:
        extra_context = {}

    view_links = []
    for view in registry.views(self.model, 'object'): 

        url_name = 'admin:%s_%s_%s' % (self.model._meta.app_label, 
                                 self.model._meta.module_name, 
                                 view.__name__)

        view_links.append( 
            (reverse(url_name, args=(object_id,) ),
             getattr(view, 'short_description', view.__name__),
             )
            )

    extra_context['views'] = view_links

    return super(self.__class__, self).change_view(
        request, object_id, extra_context=extra_context)

def changelist_view(self, request, extra_context=None):
    """Custom changelist_view, including model_views in the context."""

    if extra_context is None:
        extra_context = {}

    view_links = []
    for view in registry.views(self.model, 'model'):

        url_name = 'admin:%s_%s_%s' % (self.model._meta.app_label, 
                                 self.model._meta.module_name, 
                                 view.__name__)
        view_links.append( 
            (reverse(url_name),
             getattr(view, 'short_description', view.__name__),
             )
            )

    extra_context['views'] = view_links

    return super(self.__class__, self).changelist_view(
        request, 
        extra_context=extra_context)

def render_response(self, request, template_name, context, obj=None):

    opts = self.model._meta
    app_label = opts.app_label
    ordered_objects = opts.get_ordered_objects()

    context.update({
        'has_add_permission': self.has_add_permission(request),
        'has_change_permission': self.has_change_permission(request, obj),
        'has_delete_permission': self.has_delete_permission(request, obj),
        'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
        'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
        'ordered_objects': ordered_objects,
        'opts': opts,
        'content_type_id': ContentType.objects.get_for_model(self.model).id,
        'save_as': self.save_as,
        'save_on_top': self.save_on_top,
        'root_path': self.admin_site.root_path,
        'app_label': opts.app_label,
        'is_popup': request.REQUEST.has_key('_popup'),
    })
    context_instance = template.RequestContext(
        request, 
        current_app=self.admin_site.name)

    return render_to_response(template_name, context, 
                              context_instance=context_instance)


def instrument(admin_class):
    """Return an instrumented sub-class of admin_class that supports
    dingo's dependency injection."""

    subklass_dict = dict(
        get_urls = get_urls,
        changelist_view = changelist_view,
        change_view = change_view,
        render_response = render_response,
        )

    # create our new class and return it
    instrumented_admin = type(admin_class.__name__, 
                              (admin_class,),
                              subklass_dict)

    return instrumented_admin

ModelAdmin = instrument(admin.ModelAdmin)
