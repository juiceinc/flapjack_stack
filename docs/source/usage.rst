Usage
=====
flapjack_stack is way to allow stacked  options to be handled via a variety of
different sources. Currently, it supports Python objects, Python files,
YAML files, and OS environment variables. These attributes are stored
by layer in a list or if you prefer a stack. This results in the ability to
have composible attributes applying different layered based on deployment,
usage, or any other reason you desire. These attributes are then returned from
them right most item in the list (or top if you view as a stack) in which
they are found.

**Attributes Names**

  Please use all UPPER case setting names as it is a clear indicator to those
  behind you that this is not a normal attribute to be set at will.

Getting Started
---------------

To use flapjack_stack you start by importing the FlapjackStack object and
creating and instance of it. As shown below:::

    from flapjack_stack import FlapjackStack
    stack = FlapjackStack()

Adding Attributes from a File
-----------------------------
Python files containing the structure KEY=VALUE can be read into a new layer by
doing the following: As an example, if we had a file named our_file.py with
the contents below:::

    COOKIES="YUM"

and loaded it into stack by::

    stack.add_layer_from_file('/path/to/our_file.py')

This would result in stack looking like:

===== ======
Layer Source
===== ======
1     loaded from '/path/to/file'
Base  Empty created during init
===== ======

The same approach applies to YAML files. If we had a file named our_file.yaml
with the contents below:::

    ---
    COOKIES: 'YUM'

and loaded it into stack by::

    stack.add_layer_from_file('/path/to/our_file.yaml')

This would result in stack looking like:

===== ======
Layer Source
===== ======
1     loaded from '/path/to/file'
Base  Empty created during init
===== ======

Adding Attributes from an Object
--------------------------------
Perhaps you already have a Python object that you'd like to load into
the stack:::

    class Thing:
        def __init__(self):
            self.COOKIES = "YUMMY"
    thing = Thing()
    stack.add_layer(thing)

This would result in stack looking like:

===== ======
Layer Source
===== ======
2     load from thing object
1     loaded from '/path/to/file'
Base  Empty created during init
===== ======

Adding Attributes from Environment Variables
--------------------------------------------
One odd piece of difference about OS environment variables is that
flapjack_stacks only checks for environment variables that match the name of
attributes already in the stack at any layer prefixed with ``FJS_``. It also only
performs this check when you call the function, so changing them after the call
will not change your stack. For example:::

    stack.add_layer_from_env()

Right now would only look for ``FJS_COOKIES``.

This would result in stack looking like:

===== ======
Layer Source
===== ======
3     loaded from env
2     loaded from thing object
1     loaded from '/path/to/file'
Base  Empty created during init
===== ======

Accessing a Attribute
---------------------
To use your attribute, you simple access them like a class attribute. In our
example:::

    stack.COOKIES

Attempting to load an attribute would result in a check in the right most layer,
which is our example is Layer 3 from the environment variables for that attribute
name, and assuming we didn't set ``FJS_COOKIES`` prior to loading the environment
variables, it would then search Layer 2. Layer 2 (the thing object) set
``COOKIES`` to ``YUMMY`` so that is what we would get back. If not found, this
continues all the way down to the base layer, and then an
:py:class:`exceptions.AttributeError` will be raised.
