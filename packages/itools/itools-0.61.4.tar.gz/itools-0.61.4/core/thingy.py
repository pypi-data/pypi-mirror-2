# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Juan David Ibáñez Palomar <jdavid@itaapy.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the Standard Library
from sys import _getframe
from types import FunctionType

# Import from itools
from lazy import lazy


"""
This module implements what we call so far a "thingy", till we find a better
name.

From a semantical point of view a thingy is an abstraction of classes and
instances.  From an implementation point of view thingies are Python classes
that when instantiated create new classes, instead of class instances.

There are two ways to create a thingy:

  (1) Statically
  class my_thingy(thingy):
      ...

  (2) Dynamically
  my_thingy = thingy(...)

"""



class thingy_type(type):

    def __new__(mcs, class_name, bases, dict):
        """
        This method is called when a thingy is created "statically":

            class A(thingy):
               ...
        """
        # We don't have instance methods
        for name, value in dict.items():
            # There are not instance methods
            if type(value) is FunctionType and name != '__new__':
                value = classmethod(value)
                dict[name] = value

            # Ideally Python should support something like this:
            #
            # class A(object):
            #     x = B(...)
            #     def x.f(self):
            #         ...
            #
            #     # Or better
            #     x.f = func (self):
            #         ...
            #
            # But unfortunately it does not; so thingies work-around this
            # limit using a naming convention (and metaclasses):
            #
            # class A(thingy):
            #     x = thingy()
            #     def x__f(self):
            #         ...
            #
            if '__' in name and name[0] != '_' and name[-1] != '_':
                source_name = name
                name, rest = name.split('__', 1)
                sub = dict.get(name)
                if issubclass(type(sub), thingy_type):
                    # Closure
                    name = rest
                    while '__' in name:
                        subname, rest = name.split('__', 1)
                        aux = getattr(sub, subname, None)
                        if not issubclass(type(aux), thingy_type):
                            break
                        sub, name = aux, rest

                    setattr(sub, name, value)
                    del dict[source_name]
                    # Fix the name
                    if type(value) is classmethod:
                        value.__get__(None, dict).im_func.__name__ = name
                    elif type(value) is thingy_property:
                        value.__name__ = name
                    elif type(value) is thingy_lazy_property:
                        value.__name__ = name


        # Make and return the class
        return type.__new__(mcs, class_name, bases, dict)



class thingy(object):

    __metaclass__ = thingy_type


    def __new__(cls, *args, **kw):
        """
        This method is called when a thingy is created "dynamically":

            thingy(...)
        """
        # Make the new class
        name = '[anonymous] from %s.%s' % (cls.__module__, cls.__name__)
        new_class = type.__new__(thingy_type, name, (cls,), kw)
        # Fix the module so repr(...) gives something meaningful
        new_class.__module__ = _getframe(1).f_globals.get('__name__')
        # Initialize
        new_class.__init__(*args, **kw)
        # Ok
        return new_class


    def __init__(self, *args, **kw):
        pass



class thingy_property(lazy):

    def __get__(self, instance, owner):
        return self.meth(owner)



class thingy_lazy_property(lazy):

    def __get__(self, instance, owner):
        name = self.__name__
        for cls in owner.__mro__:
            if name in cls.__dict__:
                name = self.meth.func_name
                value = self.meth(owner)
                setattr(owner, name, value)
                return value

