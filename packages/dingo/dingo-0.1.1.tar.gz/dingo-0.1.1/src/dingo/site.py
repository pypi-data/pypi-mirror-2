from django.contrib.admin.sites import AdminSite
import django.contrib.admin

import modeladmin

class DingoAdminSite(AdminSite):

    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Registers the given model(s) with the given admin class.

        The model(s) should be Model classes, not instances.

        If an admin class isn't given, it will use ModelAdmin (the default
        admin options). If keyword arguments are given -- e.g., list_display --
        they'll be applied as options to the admin class.

        If a model is already registered, this will raise AlreadyRegistered.
        """

        # use our customized version of ModelAdmin if no class is specified
        if admin_class is None:
            admin_class = modeladmin.ModelAdmin
        else:
            # otherwise if this is a "normal" ModelAdmin, instrument it
            admin_class = modeladmin.instrument(admin_class)
        
        # call the super class implementation
        return super(DingoAdminSite, self).register(model_or_iterable, 
                                                    admin_class=admin_class,
                                                    **options)

