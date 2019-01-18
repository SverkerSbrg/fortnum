===================
Welcome to Fortnum!
===================

Fortnum is a package to help you keep track of (at runtime) static information such as the choices for your database.
This problem has many solutions from a list of strings to using an Enum and for the simple cases one of these solutions
is most likely the best. Fortnum adds value when you want to describe information in a tree or graph structure or want
each choice to be associated with more information or even other entities in your domain
 - Make defining object expressive
 - Make it easy to add information to each defined object
 - Make it easy to build hierarchies of information
 - Make it easy to add two-way references between entities

A fortnum can be defined in two ways, either using class syntax which offers all functionality

.. literalinclude:: examples/introduction.py
    :lines: 4-5

or as a simplified one liner for the simple cases

.. literalinclude:: examples/introduction.py
    :lines: 8

The two ways are equivalent and which way is preferable depends on your preference and the complexity fortnum you are
    defining.


Fortnum makes it easy to define collections. All fortnums declared as class variables will automatically be registered
as children, and a reference from the child to the parent will be added.

.. literalinclude:: examples/introduction.py
    :lines: 11-17

The collections are ordered, and the ordering can be used to compare or sort the fortnums within the collection

.. literalinclude:: examples/introduction.py
    :lines: 20-27




.. At its core a fortnum is just a string. We refer to this sting as the "key". This key is either derived from the name of
the class (when using the class syntax) or from the first argument when the constructor is used. Two fortnums with the
same key are considered equal