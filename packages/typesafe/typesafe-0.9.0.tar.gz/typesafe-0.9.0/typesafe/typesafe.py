#
# By Krister Hedfors
#
# Initially based on ActiveState recipe:
#  http://code.activestate.com/recipes/454322-type-checking-decorator/


__usage = '''
    Usage:
    from typesafe import hard_types, soft_types
    or
    from typesafe import *

    @hard_types( name=str, age=(int,float))
    def func_or_method(name, age):
        pass

    @hard_types(dict( name=str, age=(int,float) ))
    def func_or_method(name, age):
        pass
'''
__hard_types_doc = '''
    The @hard_types() decorator raises HardTypesException unless
    specified arguments are of the specified type or types:
    @hard_types(argname=type, [...])
    @hard_types(argname=types, [...])
'''
__soft_types_doc = '''
    The @soft_types() decorator raises SoftTypesException unless
    specified argument types match, or are subtypes, of the specified
    type or types. 
    @soft_types(argname=type, [...])
    @soft_types(argname=types, [...])
'''
__doc__ = __usage + __hard_types_doc + __soft_types_doc


import unittest
import doctest

from functools import wraps

from types import FunctionType,  MethodType



class TypeSafeException(Exception): pass

class HardTypesException(TypeSafeException): pass
class SoftTypesException(TypeSafeException): pass



class TypeSafeValidator(dict):
    def __init__(self, ht={}):
        dict.__init__(self)
        self.update(ht)

    def validate(self, key, val):
        if self.controls_arg(key):
            cmp = self.get_types(key)
            if self.compare(cmp, key, val):
                self.throw(cmp, key, val)

    def validate_all(self, d={}, **kw):
        kw.update(d)
        for key, val in kw.iteritems():
            self.validate(key, val)

    def throw(self, cmp, key, val):
        magic = 'XIRFXORF'
        argname = key
        argtype = str(type(val)).replace(' ', magic)
        cmp     = str(cmp).replace(' ', magic)
        error = 'argname  = %s\nrequired = %s\n\ngot type = %s\ngot val  = %s\n' %\
                (argname, cmp,  argtype,  val)
        error = error.replace(magic, ' ')
        if self.my_exception is HardTypesException:
            error = '\n\n  @hard_types() exception\n\n' + error
        elif self.my_exception is SoftTypesException:
            error = '\n\n  @soft_types() exception\n\n' + error
        raise self.my_exception(error)

    def get_types(self, argname):
        return self[argname]

    def controls_arg(self, argname):
        return self.has_key(argname)
    
    def args_and_types(self):
        for (key, val) in self.iteritems():
            yield (key, val)


class HardTypes(TypeSafeValidator):
    my_exception = HardTypesException
    def compare(self, cmp, key, val):
        valtype = type(val)
        if type(cmp) in (tuple, list):
            if not valtype in cmp:
                return 1
        else:
            if not valtype is cmp:
                return 1
        return 0

class SoftTypes(TypeSafeValidator):
    my_exception = SoftTypesException
    def compare(self, cmp, key, val):
        valtype = type(val)
        if type(cmp) in (tuple, list):
            if not isinstance(val, cmp):
                return 1
        else:
            if not isinstance(val, cmp):
                return 1
        return 0

__tmp = HardTypes()
HardTypesType = type(__tmp)
__tmp = SoftTypes()
SoftTypesType = type(__tmp)
del __tmp
    



def build_type_validating_decorator(validator_class):
    def validator(d={}, **ht):
        if not type(d) is dict:
            error = 'Invalid use of @hard_types / @soft_types.'
            error += __usage
            raise TypeSafeException(error)
        ht.update(d)

        ht = validator_class(ht)

        def _validator(func):
            if hasattr(func, "wrapped_args"):
                wrapped_args = getattr(func, "wrapped_args")
            else:
                code = func.func_code
                wrapped_args = list(code.co_varnames[:code.co_argcount])


            @wraps(func)
            def __validator(*args, **kwargs):
                for arg_index, arg_name in enumerate(wrapped_args):
                    if len(args) > arg_index:
                        arg = args[arg_index]
                        ht.validate(arg_name, arg)
                    else:
                        if arg_name in kwargs:
                            arg = kwargs[arg_name]
                            ht.validate(arg_name, arg)

                return func(*args, **kwargs)

            __validator.wrapped_args = wrapped_args
            return __validator
        return _validator
    return validator


hard_types = build_type_validating_decorator(HardTypes)
soft_types = build_type_validating_decorator(SoftTypes)

hard_types.__doc__ = __hard_types_doc
soft_types.__doc__ = __soft_types_doc

__all__ = [
    'TypeSafeException',
    'HardTypesException',
    'SoftTypesException',
    #'HardTypesType',
    #'SoftTypesType',
    #'HardTypes',
    #'SoftTypes',
    'hard_types',
    'soft_types',
]

