============================
Using the flufl.i18n library
============================

Set up
======

There are two basic ways that your application can set up translations using
this library.  The simple initialization will work for most applications,
where there is only one language context for the entire run of the
application.  The more complex initialization works well for applications like
servers that may want to use multiple language contexts during their
execution.


Single language contexts
------------------------

If your application only needs one language context for its entire execution,
you can use the simple API to set things up.

    >>> from flufl.i18n import initialize

The library by default uses the ``$LANG`` and ``$LOCPATH`` environment
variables to set things up::

    >>> # The testing 'xx' language rot13's the source string.
    >>> import os
    >>> import flufl.i18n.testing.messages

    >>> os.environ['LANG'] = 'xx'
    >>> os.environ['LOCPATH'] = os.path.dirname(
    ...     flufl.i18n.testing.messages.__file__)

Now you just need to call the ``initialize()`` function with the application's
name and you'll get an object back that you can assign to the ``_()`` function
for run-time translations.

    >>> _ = initialize('flufl')
    >>> print _('A test message')
    N grfg zrffntr


Multiple language contexts
--------------------------

Some applications, such as servers, are more complex; they need multiple
language contexts during their execution.  The first thing you should do is
import the global registry::

    >>> from flufl.i18n import registry

    >>> # Unregister the application domain used earlier.  Also, clear the
    >>> # environment settings from above.
    >>> registry._registry.clear()
    >>> del os.environ['LANG']
    >>> del os.environ['LOCPATH']

Next, decide on a strategy for finding your application's catalogs when given
a language code.  ``flufl.i18n`` comes with a couple of fairly simple ones.
One looks up catalogs from within the package directory using GNU gettext's
convention.  The base directory for the catalogs is rooted in a subpackage.

    >>> from flufl.i18n import PackageStrategy
    >>> import flufl.i18n.testing.messages

The first argument is the application name, which must be unique among all
registered strategies.  The second argument is the package where the
translations can be found.

    >>> strategy = PackageStrategy('flufl', flufl.i18n.testing.messages)

Once you have the desired strategy, register this with the global registry.
The registration process returns an application object which can be used to
look up language codes.

    >>> application = registry.register(strategy)

The application object keeps track of a current translation catalog, and
exports method which you can bind to the *underscore* function in your module
globals for convenient gettext usage.  By doing so, at run time, ``_()`` will
always translate the string argument to the current catalog's language.

    >>> _ = application._

By default the application just translates the source string back into the
source string.  I.e. it is a null translator.

    >>> print _('A test message')
    A test message

And it has no language code.

    >>> print _.code
    None

If your application uses more than one language, you can temporarily push a
new language context to the top of the stack, which automatically rebinds the
underscore function to the language's catalog.  If your application only uses
one language, just do this once in your initialization code::

    >>> _.push('xx')
    >>> print _.code
    xx

    >>> # The testing 'xx' language rot13's the source string.
    >>> print _('A test message')
    N grfg zrffntr

Pop the current language to return to the default.  Once you're at the bottom
of the stack, more pops will just give you the default translation::

    >>> _.pop()
    >>> print _.code
    None

    >>> print _('A test message')
    A test message

The underscore method has a context manager called ``using`` which can be used
to temporarily set a new language inside a ``with`` statement::

    >>> with _.using('xx'):
    ...     print _('A test message')
    N grfg zrffntr

    >>> print _('A test message')
    A test message

These ``with`` statements are nestable::

    >>> with _.using('xx'):
    ...     print _('A test message')
    ...     with _.using('yy'):
    ...         print _('A test message')
    ...     print _('A test message')
    N grfg zrffntr
    egassem tset A
    N grfg zrffntr

    >>> print _('A test message')
    A test message

You can set the bottom language context, which replaces the default null
translation::

    >>> _.default = 'xx'
    >>> print _('A test message')
    N grfg zrffntr

    >>> _.pop()
    >>> print _.code
    xx

    >>> print _('A test message')
    N grfg zrffntr

    >>> with _.using('yy'):
    ...     print _('A test message')
    egassem tset A

    >>> print _('A test message')
    N grfg zrffntr


Usage
=====

As you can see from the example above, using the library is very simple.  You
just put the string to translate inside the underscore function.  What if your
source strings need placeholders for other runtime information?

In that case, you use `PEP 292`_ style substitution strings as arguments to
the underscore function.  As a useful convenience, substitutions are taken
from the locals and globals of the function doing the translation.

    >>> ordinal = 'first'
    >>> def print_it(name):
    ...     print _('The $ordinal test message $name')

In this example, when ``print_it()`` is called, the ``$ordinal`` placeholder
is taken from globals, while the ``$name`` placeholder is taken from the
function locals (i.e. the arguments).  With no language context in place, the
source string is printed unchanged, except that the substitutions are made::

    >>> # Reset the language context.
    >>> del _.default
    >>> print _.code
    None

    >>> print_it('Anne')
    The first test message Anne

When a substitution is missing, rather than raise an exception, the $variable
is used unchanged.

    >>> del ordinal
    >>> print_it('Bart')
    The $ordinal test message Bart

When there is a language context in effect, the substitutions happen after
translation.

    >>> ordinal = 'second'
    >>> with _.using('xx'):
    ...     print_it('Cris')
    second si n grfg zrffntr Cris

Some languages change the order of the substitution variables, but of course
there is no problem with that.

    >>> ordinal = 'third'
    >>> with _.using('yy'):
    ...     print_it('Dave')
    Dave egassem tset third eht

Locals always take precedence over globals::

    >>> def print_it(name, ordinal):
    ...     print _('The $ordinal test message $name')

    >>> with _.using('yy'):
    ...     print_it('Elle', 'fourth')
    Elle egassem tset fourth eht


.. _`PEP 292`: http://www.python.org/dev/peps/pep-0292/

.. toctree::

    strategies.txt
    expand.txt
