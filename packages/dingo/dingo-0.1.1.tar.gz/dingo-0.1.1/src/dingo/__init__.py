import django.contrib.admin
import site
django.contrib.admin.site = site.DingoAdminSite()

from decorators import object_view, model_view, short_description
