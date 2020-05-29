class Former(object):
    """
    Class for dynamically adding data attributes
 
    """
    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            if hasattr(self, name):
                raise AttributeError("Conflict error: Attribute '%a' is part of the '%b'" % (name, self.__class__.__name__))
            else:
                setattr(self, name, value)

    def add_atr(self, name, value):
        setattr(self, name, value)