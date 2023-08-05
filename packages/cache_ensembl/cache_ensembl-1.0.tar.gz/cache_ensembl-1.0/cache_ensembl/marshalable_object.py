#!/usr/bin/env python
from keyword import iskeyword as _iskeyword
from marshal import dump as _dump, load as _load
import sys as _sys

def marshalable_object(typename, field_names, verbose=False):
    """Returns a new object with named fields.

    >>> Point = marshalable_object('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    """

    # Parse and validate the field names.  Validation serves two purposes,
    # generating informative error messages and preventing template injection attacks.
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split() # names separated by whitespace and/or commas
    field_names = tuple(map(str, field_names))
    for name in (typename,) + field_names:
        if not all(c.isalnum() or c=='_' for c in name):
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)
    seen_names = set()
    for name in field_names:
        if name.startswith('_'):
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    # Create and fill-in the class template
    numfields = len(field_names)
    argtxt = repr(field_names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
    reprtxt = ', '.join('%s=%%r' % name for name in field_names)
    dicttxt = ', '.join('%r: t[%d]' % (name, pos) for pos, name in enumerate(field_names))
    template = '''class %(typename)s(object):
    '%(typename)s(%(argtxt)s)' \n
    __slots__ = %(field_names)r \n
    #_____________________________________________________________________________________
    #
    #   __init__
    #_____________________________________________________________________________________
    def __init__(self, %(argtxt)s):
        """
        Initialise
        """
        self._do_init(%(argtxt)s)

    def _as_tuple (self):
        """
        returns data as a list
        """
        return tuple(getattr(self, self.__slots__[i]) for i in range(%(numfields)d))

    def _as_dict (self):
        """
        returns data as a list
        """
        return dict(zip(%(field_names)s, tuple(getattr(self, self.__slots__[i]) for i in range(%(numfields)d))))

    def _do_init (self, *data):
        """
        delegate from __init__ to handle variable number of arguments
        """
        if len(data) != %(numfields)d:
            raise TypeError('%(typename)s(%(argtxt)s): Expected %(numfields)d arguments, got %%d' %% len(data))
        for i in range(%(numfields)d):
            setattr(self, self.__slots__[i], data[i])

    def __eq__(self, other):
       if type(other) == %(typename)s:
           return cmp(self, other) == 0
       else:
           return False

    def __cmp__(self, other):
        if type(other) != %(typename)s:
           return -1
        for i in range(%(numfields)d):
            c = cmp(getattr(self, self.__slots__[i]) != getattr(other, self.__slots__[i]))
            if c:
                return c
        return 0
    #_____________________________________________________________________________________
    #
    #   dump
    #_____________________________________________________________________________________
    def dump(self, data_file):
        """
        dump
        """
        for i in range(%(numfields)d):
            dump(getattr(self, self.__slots__[i]), data_file)

    #_____________________________________________________________________________________
    #
    #   load
    #_____________________________________________________________________________________
    @staticmethod
    def load(data_file):
        """
        load
        """
        data = []
        for i in range(%(numfields)d):
            data.append(load(data_file))

        return %(typename)s(  *data)

    #_____________________________________________________________________________________
    #
    #   __repr__
    #_____________________________________________________________________________________
    def __repr__ (self):
        return ('%(typename)s(%(reprtxt)s)' %% self._as_tuple())\n
    \n\n''' % locals()
    if verbose:
        print template

    # Execute the template string in a temporary namespace and
    # support tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(dump=_dump, load=_load, __name__='marshalable_object_%s' % typename)
    try:
        exec template in namespace
    except SyntaxError, e:
        raise SyntaxError(str(e) + ':\n' + template)
    result = namespace[typename]

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in enviroments where
    # sys._getframe is not defined (Jython for example).
    if hasattr(_sys, '_getframe'):
        result.__module__ = _sys._getframe(1).f_globals['__name__']

    return result


#_____________________________________________________________________________________

#   dump_dict_of_objects
#   load_dict_of_objects

#_____________________________________________________________________________________
def dump_dict_of_objects (dict_of_objects, data_file):
    _dump(len(dict_of_objects), data_file)
    for k, v in dict_of_objects.iteritems():
        _dump(k, data_file)
        v.dump(data_file)

def load_dict_of_objects (data_file, marshalable_class):
    dict_of_objects = dict()
    cnt_objects = _load(data_file)
    for i in range(cnt_objects):
        k = _load(data_file)
        dict_of_objects[k] = marshalable_class.load(data_file)
    return dict_of_objects


#_____________________________________________________________________________________

#   dump_dict_of_object_lists
#   load_dict_of_object_lists

#_____________________________________________________________________________________
def dump_dict_of_object_lists (dict_of_objects, data_file):
    _dump(len(dict_of_objects), data_file)
    for k, v in dict_of_objects.iteritems():
        _dump(k, data_file)
        _dump(len(v), data_file)
        for vv in v:
            vv.dump(data_file)

def load_dict_of_object_lists (data_file, marshalable_class):
    dict_of_objects = dict()
    cnt_objects = _load(data_file)
    for i in range(cnt_objects):
        k = _load(data_file)
        dict_of_objects[k] = []
        cnt_list = _load(data_file)
        for j in range(cnt_list):
            dict_of_objects[k].append(marshalable_class.load(data_file))
    return dict_of_objects



if __name__ == '__main__':
    # verify that instances can be marshaled
    Point = marshalable_object('Point', ' x y a b')
    p = Point(x=10, y=20, a=30, b="")
    print p
    import marshal
    f =open("temp", "wb")
    p.dump(f)
    f.close()
    f =open("temp")
    p2 = Point.load(f)
    print p2


