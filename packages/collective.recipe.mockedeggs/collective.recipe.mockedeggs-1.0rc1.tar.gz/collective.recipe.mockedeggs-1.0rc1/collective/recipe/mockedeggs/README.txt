Usage
=====

Sometimes you can't add eggs through your buildout engine or easy_install, for
example if some dev libraries are lacking on your system, or are too old, etc.

But you can install module directly on your system using your system's packaging
utility (``port install python-xxx``, ``apt-get install python-xxx`` or with
``.msi`` installers for Windows. In example ``python-ldap`` or ``lxml`` are
somehow difficult to install on Windows using source eggs, and are usually
available as binary installers.

Then, though you get all you need in your python environment, your buildout may
fail because an egg is missing.

This recipe will make buildout believe that such missing eggs are available and
installed, when your app will use the system wide Pyhton packages you installed
by your way.

Yes, I know you should usually not do this but sometimes there's no other (easy)
way to have your buildout completed.

How-to
======

You have to add **ON TOP OF YOUR PARTS** a ``collective.recipe.mockedeggs``
recipe part::

    [buildout]
    parts = mocked-eggs
            other parts...

    [mocked-eggs]
    recipe=collective.recipe.mockedeggs

The recipe supports the following options:

mocked-eggs
    The list of eggs you want to mock, with their version number, as for
    example::

        mocked-eggs =
            python-ldap=2.3.10
            Markdown = 1.7


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = mocked-eggs-test
    ...         zopepy
    ...
    ... eggs = mocked1
    ...        mocked2
    ...
    ... [mocked-eggs-test]
    ... recipe = collective.recipe.mockedeggs
    ... mocked-eggs =
    ...      mocked1=1.0
    ...      mocked2=  2.0
    ...
    ... [zopepy]
    ... recipe = zc.recipe.egg
    ... interpreter = zopepy
    ... eggs = mocked1
    ...        mocked2
    ...
    ... """)

Running the buildout gives us ::

    >>> print 'start...\n', system(buildout)
    start...
    Installing mocked-eggs-test.
    mocked-eggs-test: Mocked eggs mocked1, mocked2.
    ...

    >>> import os
    >>> os.path.exists('mocked-eggs-test')
    True
    >>> os.path.exists('mocked-eggs-test/fake-mocked1')
    True
    >>> os.path.exists('mocked-eggs-test/fake-mocked2')
    True

    >>> setup1 = open('mocked-eggs-test/fake-mocked1/setup.py').read()
    >>> '1.0' in setup1
    True
    >>> "'mocked1'" in setup1
    True
    >>> binary = open('bin/zopepy', 'r').read()
    >>> 'mocked-eggs-test/fake-mocked1' in binary
    True
