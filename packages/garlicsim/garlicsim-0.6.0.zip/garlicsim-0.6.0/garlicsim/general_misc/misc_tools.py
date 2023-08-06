# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines miscellaneous tools.'''

import re
import math
import types


def is_subclass(candidate, base_class):
    '''
    Check if `candidate` is a subclass of `base_class`.
    
    You may pass in a tuple of base classes instead of just one, and it will
    check whether `candidate` is a subclass of any of these base classes.
    
    The advantage of this over the built-in `issubclass` is that it doesn't
    throw an exception if `candidate` is not a type. (Python issue 10569.)
    '''
    return isinstance(candidate, (type, types.ClassType)) and \
           issubclass(candidate, base_class)


def frange(start, finish=None, step=1.):
    '''
    Make a `list` containing an arithmetic progression of numbers.

    This is an extension of the builtin `range`; It allows using floating point
    numbers.
    '''
    if finish is None:
        finish, start = start, 0.
    else:
        start = float(start)

    count = int(math.ceil(finish - start)/step)
    return (start + n*step for n in range(count))
    

def getted_vars(thing, _getattr=getattr):
    '''
    The `vars` of an object, but after we used `getattr` to get them.
    
    This is useful because some magic (like descriptors or `__getattr__`
    methods) need us to use `getattr` for them to work. For example, taking
    just the `vars` of a class will show functions instead of methods, while
    the "getted vars" will have the actual method objects.
    
    You may provide a replacement for the built-in `getattr` as the `_getattr`
    argument.
    '''
    # todo: can make "fallback" option, to use value from original `vars` if
    # get is unsuccessful.
    my_vars = vars(thing)
    return dict((name, _getattr(thing, name)) for name in my_vars.iterkeys())



_ascii_variable_pattern = re.compile('^[a-zA-Z_][0-9a-zA-Z_]*$')
def is_legal_ascii_variable_name(name):
    '''Return whether `name` is a legal name for a Python variable.'''
    return bool(_ascii_variable_pattern.match(name))


def get_actual_type(thing):
    '''
    Get the actual type (or class) of an object.
    
    This is used instead of `type(thing)` for compaibility with old-style
    classes.
    '''
    
    return getattr(thing, '__class__', None) or type(thing)
    # Using `.__class__` instead of `type` because of goddamned old-style
    # classes. When you do `type` on an instance of an old-style class, you
    # just get the useless `InstanceType`. But wait, there's more! We can't
    # just take `thing.__class__` because the old-style classes themselves,
    # i.e. the classes and not the instances, do not have a `.__class__`
    # attribute at all! Therefore we are using `type` as a fallback.
    #
    # I don't like old-style classes, that's what I'm saying.
    
    
def is_number(x):
    '''Return whether `x` is a number.'''
    try:
        x + 1
    except Exception:
        return False
    else:
        return True
    
    