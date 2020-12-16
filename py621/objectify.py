class DictProxy(object): # From https://stackoverflow.com/a/31569634/14422669
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, key):
        return wrap(self.obj[key])

    def __getattr__(self, key):
        try:
            return wrap(getattr(self.obj, key))
        except AttributeError:
            try:
                return self[key]
            except KeyError:
                raise AttributeError(key)

class ListProxy(object):
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, key):
        return wrap(self.obj[key])

def wrap(value):
    if isinstance(value, dict):
        return DictProxy(value)
    if isinstance(value, (tuple, list)):
        return ListProxy(value)
    return value