
class ModelAdmin__old(admin.ModelAdmin):
    """Enhanced ModelAdmin whcih attempts to streamline the addition of
    additional views/actions in the admin."""

    instance_actions = []
    """Actions which may be performed against a single instance of the model, 
    formatted as a list of tuples consisting of (name, view_method_name).  

    The named view method should take the request and a single positional 
    argument, the pk.  The method may be decorated with a short_description 
    which will be used in the web interface."""

    class_actions = []
    """Actions which may be performed against all instances of the model, 
    formatted as a list of tuples consisting of (name, view_method_name).  

    The named view method should take no positional or keyword arguments,
    only the request.  The method may be decorated with a short_description 
    which will be used in the web interface."""

    
