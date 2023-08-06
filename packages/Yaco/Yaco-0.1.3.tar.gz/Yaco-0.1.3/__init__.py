"""
Yaco
----

Yaco provides a `dict` like structure that can be serialized to & from
`yaml <http://www.yaml.org/>`_. Yaco objects behave as dictionaries
but also allow attribute access (loosely based on this `recipe <
http://code.activestate.com/recipes/473786/>`_). Sublevel dictionaries
are automatically converted to Yaco objects, allowing sublevel
attribute access, for example::

    >>> x = Yaco()
    >>> x.test = 1
    >>> x.sub.test = 2
    >>> x.sub.test
    2

Note that sub-dictionaries do not need to be initialized. This has as
a consequence that requesting uninitialized items automatically return
an empty Yaco object (inherited from a dictionary).

Yaco can be `found <http://pypi.python.org/pypi/Yaco/0.1.1>`_ in the
`Python package index <http://pypi.python.org/pypi/>`_ and is also
part of the `Moa source distribution
<https://github.com/mfiers/Moa/tree/master/lib/python/Yaco>`_


"""

import os
import yaml

class Yaco(dict):
    """
    Loosely based on http://code.activestate.com/recipes/473786/ (r1)

    >>> v= Yaco()
    >>> v.a = 1
    >>> assert(v.a == 1)
    >>> assert(v['a'] == 1)
    >>> v= Yaco({'a':1})
    >>> assert(v.a == 1)
    >>> assert(v['a'] == 1)
    
    """
    
    def __init__(self, data={}):
        """
        Constructor
        
        :param data: data to initialize the Yaco structure with
        :type data: dict
        """
        dict.__init__(self)
        if type(data) == type("string"):
            data = yaml.load(data)
        self.update(data)

    def __str__(self):
        """
        Map the structure to a string
        
        >>> v= Yaco({'a':1})
        >>> assert(str(v.a) == '1')
        """
        return str(self.get_data())

    def __setitem__(self, key, value):
        """
        Set the value of a key
        
        >>> v= Yaco()
        >>> v.a = 18
        >>> assert(v.a == 18)

        >>> v.a = 72
        >>> assert(v.a == 72)

        >>> v.a = {'b' : 5}
        >>> assert(v.a.b == 5)        

        >>> v.a = {'c' : {'d' : 19}}
        >>> assert(v.a.b == 5)
        >>> assert(v.a.c.d == 19)
        >>> assert(v.a['c'].d == 19)

        >>> #create new instances on the fly
        >>> v.e = 1

        >>> v.f.g = 14
        >>> assert(v.f.g == 14)

        >>> v.f.h.i.j.k.l = 14
        >>> assert(v.f.h.i.j.k.l == 14)

        :param key: The key to set
        :param value: The value to assign to key
        """
        
        old_value = super(Yaco, self).get(key, None)
        if isinstance(value, dict):
            #setting a dict
            if isinstance(old_value, Yaco):
                old_value.update(value)
            else:
                super(Yaco, self).__setitem__(key, Yaco(value))
        else:
            super(Yaco, self).__setitem__(key, value)
     
    def __getitem__(self, key):
        """
        >>> v= Yaco()
        >>> v.a = 18       
        >>> assert(v.a == 18)
        >>> assert(isinstance(v.a, int))
        """
        try:
            return super(Yaco, self).__getitem__(key)
        except KeyError:
            rv = Yaco()
            super(Yaco, self).__setitem__(key, rv)
            return rv
        
    def __delitem__(self, name):
        return super(Yaco, self).__delitem__(name)

    def update(self, data):
        """
        
        """
        if not data: return 
        for key, val in data.items():
            if isinstance(val, Yaco):
                raise Exception("Wow - updating with a Yaco - should not happen (%s = %s)!" % (key, val))

            old_value = super(Yaco, self).get(key, None)
            if isinstance(val, dict):
                if old_value and isinstance(old_value, Yaco):
                    old_value.update(val)
                else:
                    super(Yaco, self).__setitem__(key, Yaco(val))
            else:
                super(Yaco, self).__setitem__(key, val)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = Yaco(self)
        return ch
    
    def load(self, from_file):
        """
        Load this dict from_file

        >>> import yaml
        >>> import tempfile
        >>> tf = tempfile.NamedTemporaryFile(delete=False)
        >>> tf.write(yaml.dump({'a' : [1,2,3], 'b': 4, 'c': '5'}))
        
        """
        with open(from_file) as F:
            data = yaml.load(F)
        self.update(data)

    def get_data(self):
        """
        Prepare & parse data for export             
        """
        data = {}
        for k in self.keys():
            if k[0] == '_': continue
            val = self[k]
            if isinstance(val, Yaco):
                val = val.get_data()
            data[k] = val
        return data
                 
    def save(self, to_file, doNotSave=[]):
        """
        
        """        
        with open(to_file, 'w') as F:
            data = self.get_data()
            for k in data.keys():
                if k in doNotSave:
                    del data[k]
            
            F.write(yaml.dump(data, default_flow_style=False))

if __name__ == "__main__":

    import doctest
    doctest.testmod()
