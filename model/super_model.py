
class SuperModel :
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs.get(key))

    def export_dict(self, params=None):
        if not params :
            return self.__dict__
        else :
            my_dict = {}
            for a in params:
                my_dict[a] = getattr(self, a)

            return my_dict