try:
    import json
except ImportError:
    import simplejson as json

from .fields import BaseField

class Model(object):
    """The Model is the main component of micromodels. Model makes it trivial
    to parse data from many sources, including JSON APIs.

    The constructor for model takes either a native Python dictionary (default)
    or a JSON dictionary if ``is_json`` is ``True``.

    """
    class __metaclass__(type):
        '''Creates the metaclass for Model. The main function of this metaclass
        is to move all of fields into the _fields variable on the class.

        '''
        def __init__(cls, name, bases, attrs):
            cls._clsfields = {}
            for key, value in attrs.iteritems():
                if isinstance(value, BaseField):
                    cls._clsfields[key] = value

    def __init__(self, data, is_json=False):
        self._extra = {}
        if is_json:
            data = json.loads(data)
        for name, field in self._clsfields.iteritems():
            key = field.source or name
            field.populate(data.get(key))
            setattr(self, name, field.to_python())

    @property
    def _fields(self):
        return dict(self._clsfields, **self._extra)

    def add_field(self, key, value, field):
        ''':meth:`add_field` must be used to add a field to an existing
        instance of Model. This method is required so that serialization of the
        data is possible. Data on existing fields (defined in the class) can be
        reassigned without using this method.

        '''
        field.populate(value)
        setattr(self, key, field.to_python())
        self._extra[key] = field

    def to_dict(self, serial=False):
        '''A dictionary representing the the data of the class is returned.
        Native Python objects will still exist in this dictionary (for example,
        a ``datetime`` object will be returned rather than a string)
        unless ``serial`` is set to True.

        '''
        keys = (k for k in self.__dict__.keys() if k in self._fields.keys())

        if serial:
            return dict((key, self._fields[key].to_serial(getattr(self, key)))
                     for key in keys)
        else:
            return dict((key, getattr(self, key)) for key in keys)

    def to_json(self):
        '''Returns a representation of the model as a JSON string. This method
        relies on the :meth:`~micromodels.Model.to_dict` method.

        '''
        return json.dumps(self.to_dict(serial=True))
