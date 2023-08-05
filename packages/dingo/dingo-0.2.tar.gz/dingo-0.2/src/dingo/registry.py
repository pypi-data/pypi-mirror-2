_REGISTRY = {}

def register(klass, action_type, action):

    _REGISTRY.setdefault(klass, {}).setdefault(action_type, []).append(action)

def views(klass, action_type):

    return _REGISTRY.setdefault(klass, {}).setdefault(action_type, [])
