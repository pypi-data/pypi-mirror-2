import registry

def short_description(description):
    """A decorator factory which annotates the function with the
    specified description as the ``short_description`` property."""

    def sd(f):
        f.short_description = description
        return f

    return sd

class object_view(object):
    """Declare a function as an object view for a given class.
    Object views have the signature::

      f(model_admin, request, object_id).
    
    This can be used as a decorator::

      @object_view(my.django.models.Model)
      def a_view(admin, request, object_id):
          pass

    Or as a wrapper::

      def another_view(admin, request, object_id):
          pass

      another_view = object_view(my.django.models.Model)(another_view)

    """

    def __init__(self, klass):
        self._klass = klass

    def __call__(self, ob):

        registry.register(self._klass, 'object', ob)

        return ob

def model_view(object):
    """Declare a function as a model view for a given model.
    Model views have the signature::

      f(model_admin, request).
    
    This can be used as a decorator::

      @model_view(my.django.models.Model)
      def a_view(admin, request):
          pass

    Or as a wrapper::

      def another_view(admin, request):
          pass

      another_view = model_view(my.django.models.Model)(another_view)

    """
    
    def __init__(self, klass):
        self._klass = klass

    def __call__(self, ob):

        registry.register(self._klass, 'model', ob)

        return ob
