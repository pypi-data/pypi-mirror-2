A ``Reference`` is a Zope object refering to another Zope object,
called its *Target*.
The target it identified by a path relative to the parent
of the ``Reference``.
It is resolved into the target through ``restrictedTraverse``.

The attribute ``Target`` as well as the method ``getTarget`` give
the target object.

A ``Reference`` behaves almost like its target. It appears to have
(most of) its attributes and methods.
In this sense, it is very similar to Shane's ``Symlink`` product.
Unlike a ``Symlink``, however, a ``Reference`` has its own
id, title and management facilities and therefore
can be distinguished from the refered to object.
This is very difficult for a ``SymLink``;
therefore, I consider ``Reference`` safer.

On lookup, a ``Reference`` prefers its own attributes over
those of the target. This means that it behaves as a reference
and partially as its target.

Caveats
=======
There are security weaknesses: the ``setDefaultAccess('allow')``
and the ``declareObjectProtected('Access contents information')``
of ``Reference`` spill over to the target when accessed through the
reference. This is a side effect of Zope's (strange) security
policy.

In order to ensure manageability of the Reference,
``__before_publishing_traverse__`` and ``__bobo_traverse__``
are not relayed to the target.

It is very difficult (I think impossible) to emulate the
special treatment of Python Methods by acquisition.
The current implementation tries hard to emulate enough
that Python Scripts (and similar objects) get correct bindings.
However, the acquisition context is otherwise different from
how it were when directly called.

Zope toolkit (aka Zope3) adapters (this includes views) may not work
on references as you expect
because the adapters see the interfaces implemented
by the reference itself, not those of the refered to object.
