class Former(object):
    """
    Class for dynamically adding data attributes
 
    """
    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            if hasattr(self, name):
                raise AttributeError("Conflict error: Attribute %s is part of the %s" % (name, self.__class__.__name__))
            else:
                setattr(self, name, value)

    def add_atr(self, name, value):
        setattr(self, name, value)