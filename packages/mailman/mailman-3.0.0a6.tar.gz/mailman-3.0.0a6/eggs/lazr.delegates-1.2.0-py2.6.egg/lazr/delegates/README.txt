..
    This file is part of lazr.delegates.

    lazr.delegates is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    lazr.delegates is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with lazr.delegates.  If not, see <http://www.gnu.org/licenses/>.

The ``lazr.delegates`` Package
******************************

The ``lazr.delegates`` package makes it easy to write objects that delegate
behavior to another object. The new object adds some property or behavior on
to the other object, while still providing the underlying interface, and
delegating behavior.

=====
Usage
=====

The ``delegates`` function makes a class implement zero or more
interfaces by delegating the implementation to another object. In the
case of a class providing an adapter, that object will be the 'context',
but it can really be any object stored in an attribute. So while the
interfaces use an inheritance mechanism, the classes use a composition
mechanism.

For example we can define two interfaces IFoo0 <- IFoo...

    >>> from lazr.delegates import delegates
    >>> from zope.interface import Interface, Attribute
    >>> class IFoo0(Interface):
    ...     spoo = Attribute('attribute in IFoo0')

    >>> class IFoo(IFoo0):
    ...     def bar():
    ...         "some method"
    ...     baz = Attribute("some attribute")

And two classes (BaseFoo0 <- BaseFoo) that do something interesting.

    >>> class BaseFoo0:
    ...     spoo = 'some spoo'

    >>> class BaseFoo(BaseFoo0):
    ...     def bar(self):
    ...         return 'bar'
    ...     baz = 'hi baz!'

SomeClass can implement IFoo by delegating to an instance of BaseFoo
stored in the 'context' attribute. Note that ``delegates`` takes the
interface as the argument. By default, 'context' is the attribute
containing the object to which the interface implementation is
delegated.

    >>> class SomeClass(object):
    ...     delegates(IFoo)
    ...     def __init__(self, context):
    ...         self.context = context

    >>> f = BaseFoo()
    >>> s = SomeClass(f)
    >>> s.bar()
    'bar'

    >>> s.baz
    'hi baz!'

    >>> s.spoo
    'some spoo'

    >>> IFoo.providedBy(s)
    True

The ``delegates()`` function takes an optional keyword argument to change
attribute containing the object to delegate to. So an existing class,
such as SomeOtherClass, can declare the name of the attribute to which to
delegate.

    >>> class SomeOtherClass(object):
    ...     delegates(IFoo, context='myfoo')
    ...     def __init__(self, foo):
    ...         self.myfoo = foo
    ...     spoo = 'spoo from SomeOtherClass'

    >>> f = BaseFoo()
    >>> s = SomeOtherClass(f)
    >>> s.bar()
    'bar'

    >>> s.baz
    'hi baz!'

    >>> s.spoo
    'spoo from SomeOtherClass'

    >>> s.baz = 'fish'
    >>> s.baz
    'fish'

    >>> f.baz
    'fish'

The ``delegates()`` function can only be used in new-style classes. An
error is raised when a classic-style class is modified to implement an
interface.

    >>> class SomeClassicClass:
    ...     delegates(IFoo)
    Traceback (most recent call last):
    ...
    TypeError: Cannot use delegates() on a classic
        class: __builtin__.SomeClassicClass.

The ``delegates()`` function cannot be used out side of a class definition,
such as in a module or in a function.

    >>> delegates(IFoo)
    Traceback (most recent call last):
    ...
    TypeError: delegates() can be used only from a class definition.

Multiple interfaces can be specified by passing an iterable to
delegates().

    >>> class IOther(Interface):
    ...     another = Attribute("another attribute")

    >>> class BaseOtherFoo(BaseFoo):
    ...     another = 'yes, another'

    >>> class SomeOtherClass(object):
    ...     delegates([IFoo, IOther])

    >>> s = SomeOtherClass()
    >>> s.context = BaseOtherFoo()
    >>> s.another
    'yes, another'

    >>> s.baz
    'hi baz!'

    >>> s.spoo
    'some spoo'

    >>> IFoo.providedBy(s)
    True

    >>> IOther.providedBy(s)
    True

This can be convenient when decorating an existing object.

    >>> from zope.interface import implements
    >>> class MoreFoo(BaseFoo, BaseOtherFoo):
    ...     implements(IFoo, IOther)

    >>> foo = MoreFoo()

    >>> from zope.interface import providedBy
    >>> class WithExtraTeapot(object):
    ...     delegates(providedBy(foo))
    ...     teapot = 'i am a teapot'

    >>> foo_with_teapot = WithExtraTeapot()
    >>> foo_with_teapot.context = foo

    >>> foo_with_teapot.baz
    'hi baz!'

    >>> foo_with_teapot.another
    'yes, another'

    >>> foo_with_teapot.teapot
    'i am a teapot'

    >>> IFoo.providedBy(foo_with_teapot)
    True

    >>> IOther.providedBy(foo_with_teapot)
    True

==============
Implementation
==============

The Passthrough class is the implementation machinery of ``delegates()``. It
uses the descriptor protocol to implement the delegation behaviour provided by
``delegates()``. It takes at least two arguments: the name of the attribute
that is delegated, and the name of the attribute containing the object to
which to delegate.

To illustrate, p and p2 are two Passthrough instances that use the
instance assigned to 'mycontext' to call the 'foo' attribute and
the 'clsmethod' method.

    >>> from lazr.delegates import Passthrough
    >>> p = Passthrough('foo', 'mycontext')
    >>> p2 = Passthrough('clsmethod', 'mycontext')

Base is a class the implements both 'foo' and 'clsmethod'.

    >>> class Base:
    ...     foo = 'foo from Base'
    ...     def clsmethod(cls):
    ...         return str(cls)
    ...     clsmethod = classmethod(clsmethod)

Adapter is a class that has an instance of Base assigned to the
attribute 'mycontext'.

    >>> base = Base()

    >>> class Adapter:
    ...     mycontext = base

    >>> adapter = Adapter()

The Passthrough instances can get and set their prescribed attributes
when passed an instance of adapter.

    >>> p.__get__(adapter)
    'foo from Base'

    >>> p.__get__(None, Adapter) is p
    True

    >>> p2.__get__(adapter)()
    '__builtin__.Base'

    >>> p.__set__(adapter, 'new value')
    >>> base.foo
    'new value'

Passthrough does not implement __delete__. An error is raised if
it is called.

    >>> p.__delete__(adapter)
    Traceback (most recent call last):
    ...
    NotImplementedError

Passthrough's third argument (adaptation) is optional and, when provided,
should be a zope.interface.Interface subclass (although in practice any
callable will do) to which the instance is adapted before getting/setting the
delegated attribute.

    # HasNoFoo does not have a .foo attribute...
    >>> class HasNoFoo(object):
    ...     _foo = 1
    >>> no_foo = HasNoFoo()

    # ... but IHasFooAdapter uses HasNoFoo._foo to provide its own .foo, so it
    # works like an adapter for HasNoFoo into some interface that provides
    # a 'foo' attribute.
    >>> class IHasFooAdapter(object):
    ...     def __init__(self, inst):
    ...         self.inst = inst
    ...     def _get_foo(self):
    ...         return self.inst._foo
    ...     def _set_foo(self, value):
    ...         self.inst._foo = value
    ...     foo = property(_get_foo, _set_foo)

    >>> class Example(object):
    ...     context = no_foo

    >>> p = Passthrough('foo', 'context', adaptation=IHasFooAdapter)
    >>> e = Example()
    >>> p.__get__(e)
    1
    >>> p.__set__(e, 2)
    >>> p.__get__(e)
    2


===============
Other Documents
===============

.. toctree::
   :glob:

   *
   docs/*
