from typesafe import (
    hard_types,
    soft_types,
    HardTypesException,
    SoftTypesException,
)

import unittest


class IntSub(int): pass
class FloatSub(float): pass
class StringSub(str): pass


@hard_types(a=int, b=int)
def sum_int_hard(a, b):
    return a+b

@soft_types(a=int, b=int)
def sum_int_soft(a, b):
    return a+b


class Klass(object):

    @hard_types( name=(str,unicode), age=(int,float))
    def greet_hard(self, name, age):
        return 'Hello '+ name +' '+ str(age)

    @soft_types( name=(str,unicode), age=(int,float))
    def greet_soft(self, name, age):
        return 'Hello '+ name +' '+ str(age)


class Test(unittest.TestCase):

    def test_hard_types_on_func(self):

        self.assertEqual (
            sum_int_hard(33, 44),
            77
        )
        self.assertEqual (
            sum_int_hard(a=33, b=44),
            77
        )
        self.assertRaises (
            HardTypesException,
            lambda : sum_int_hard(IntSub(33), IntSub(44)),
        )
        self.assertRaises (
            HardTypesException,
            lambda : sum_int_hard(888, b=1.07)
        )
        self.assertRaises (
            HardTypesException,
            lambda : sum_int_hard(a='asd', b=777)
        )
        self.assertRaises (
            HardTypesException,
            lambda : sum_int_hard(888, 1.07)
        )

    def test_soft_types_on_func(self):

        self.assertEqual (
            sum_int_soft(33, 44),
            77
        )
        self.assertEqual (
            sum_int_soft(a=33, b=44),
            77
        )
        self.assertEqual (
            sum_int_soft(IntSub(33), b=IntSub(44)),
            77
        )
        self.assertRaises (
            SoftTypesException,
            lambda : sum_int_soft(a=888, b=1.07)
        )
        self.assertRaises (
            SoftTypesException,
            lambda : sum_int_soft('asd', 777)
        )
        self.assertRaises (
            SoftTypesException,
            lambda : sum_int_soft(888, 1.07)
        )

    def test_hard_types_on_method(self):
        
        klass = Klass()
        self.assertEqual (
            klass.greet_hard('World', 42),
            'Hello World 42'
        )
        self.assertEqual (
            klass.greet_hard(name='World', age=42.0),
            'Hello World 42.0'
        )
        self.assertEqual (
            klass.greet_hard(u'World', 42.0),
            'Hello World 42.0'
        )
        self.assertRaises (
            HardTypesException,
            lambda : klass.greet_hard(u'World', FloatSub(42.0))
        )
        self.assertRaises (
            HardTypesException,
            lambda : klass.greet_hard(name=StringSub('World'), age=42.0)
        )
        self.assertRaises (
            HardTypesException,
            lambda : klass.greet_hard(dict(), 'asd')
        )

    def test_soft_types_on_method(self):
        
        klass = Klass()
        self.assertEqual (
            klass.greet_soft('World', 42),
            'Hello World 42'
        )
        self.assertEqual (
            klass.greet_soft(name='World', age=42.0),
            'Hello World 42.0'
        )
        self.assertEqual (
            klass.greet_soft(u'World', 42.0),
            'Hello World 42.0'
        )
        self.assertEqual (
            klass.greet_soft(u'World', FloatSub(42.0)),
            'Hello World 42.0'
        )
        self.assertEqual (
            klass.greet_soft(name=StringSub('World'), age=42.0),
            'Hello World 42.0'
        )
        self.assertRaises (
            SoftTypesException,
            lambda : klass.greet_soft('World', dict(age=42))
        )


unittest.main()
