#       $Id: __init__.py,v 1.1.1.1 2010/03/17 18:25:57 dieter Exp $
# Copyright (C) 2002-2010 by Dr. Dieter Maurer <dieter@handshake.de>
# D-66571 Bubach, Illtalstr. 25, Germany
#
#			All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice and this permission
# notice appear in all copies, modified copies and in
# supporting documentation.
# 
# Dieter Maurer DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL Dieter Maurer
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
'''References

A 'Reference' is an object refering to another Zope object, called its *Target*.

It is very similar to Shanes 'Symlink' in that it behaves almost like
the target. Unlike a 'Symlink', however, a 'Reference' has its own
id, title and management facilities. Therefore, I consider it safer.

There are still security weaknesses: the 'setDefaultAccess('allow')'
and the 'declareObjectProtected('Access contents information')'
of 'Reference' spill over to the target when accessed through the
reference. This is a side effect that Zope does not allow to
protect simple attribute (such as 'title') explicitly.

In order to ensure manageability of References, some
restrictions apply:

  *  '__before_publishing_traverse__' and '__bobo_traverse__' are
     not (automatically) relayed to the target.

It is very difficult (I think impossible) to emulate the
special treatment of Python Methods by acquisition.
The current implementation tries hard to emulate enough
that Python Scripts (and similar objects) get correct bindings.
However, the acquisition context is otherwise different from
how it were when directly called.
'''

from Globals import InitializeClass, DTMLFile, Persistent
from OFS.SimpleItem import SimpleItem
from OFS.Traversable import Traversable
from App.Management import Tabs
from App.Undo import UndoSupport
from AccessControl.Owned import Owned
from AccessControl.Role import RoleManager
from AccessControl.SecurityInfo import ClassSecurityInfo
from AccessControl.Permissions import access_contents_information
from Acquisition import Implicit, aq_base, aq_parent
from ComputedAttribute import ComputedAttribute
from ExtensionClass import Base

try:
    from ExtensionClass import PythonMethodType
except ImportError:
    # a new style "ExtensionClass" (Zope 2.8 and later)
    from types import MethodType as PythonMethodType, InstanceType

from sys import stderr

def initialize(context):
    context.registerClass(Reference,
                          constructors=(manage_addReferenceForm,
                                        manage_addReference),
                          permission= 'References: add',
                          icon= "Reference.gif",
                          )


manage_addReferenceForm = DTMLFile('addForm', globals())

def manage_addReference(self, id, title, path, REQUEST=None):
    '''Add a reference to *path*. The target does not need to exist.'''
    ob= Reference(id)
    ob.edit(title,path)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

def _dictify(seq):
    d= {}
    for s in seq: d[s]= None
    return d


class Reference(SimpleItem):
    '''we did not want to inherit from 'SimpleItem' because it defines
    the stupid 'object*' methods. However, 'manage_fixupOwnershipAfterAdd'
    is so stupid that it acquires 'objectValues' when it is not defined,
    leading to an infinite loop. Therefore, we must be much more
    careful.
    '''

    meta_type = 'Reference'

    security= ClassSecurityInfo()
    security.declareObjectProtected(access_contents_information)
    security.setDefaultAccess('allow')
    security.declareProtected('References: change',
                              'edit', 'editForm',
                              )

    _max_recursion = 100
    _v_recursion= 0

    manage_options= (
        { 'label' : 'Edit', 'action' : 'editForm',},
        { 'label' : 'Target', 'action' : 'Target/manage_workspace',},
        ) + SimpleItem.manage_options
    
    def __init__(self, id):
        self.id = id

    def edit(self,title,path, REQUEST= None):
        '''set title and target path.'''
        self.title= title
        self.targetPath= path
        if REQUEST is not None:
            REQUEST.response.redirect(
                '%s/manage_workspace' % self.absolute_url()
                )

    editForm= DTMLFile('editForm', globals())

    def getTarget(self):
        '''return the target object'''
        return self.aq_parent.restrictedTraverse(self.targetPath)

    # give it a private name to easily avoid acquisition
    _getTarget= getTarget

    Target= ComputedAttribute(getTarget,1)

    _myOMIcon= ( {'title':meta_type, 'alt':meta_type, 'path':'misc_/References/Reference.gif',},)
    def om_icons(self):
        '''the list of ObjectManager icons.'''
        myI= self._myOMIcon
        try: t= self.getTarget()
        except:
            return myI + ({'title': 'missing', 'alt':'missing', 'path':'p_/broken',},)
        if hasattr(t.aq_base,'om_icons'):
            ti= t.om_icons
            if callable(ti): ti= ti() # ATT: may require safer 'callable'
            if ti: return myI + ti
        return myI + (
            {'title':t.meta_type, 'alt':t.meta_type, 'path':t.icon,},
            )


    # there are several things, we should not relay to the target,
    # because it can prevent managebility of ourself.
    # we may want more intelligent solutions than this one!
    _dontRelayToTarget= (
        '__before_publishing_traverse__',
        '__bobo_traverse__',
        )
    _dontRelayToTarget= _dictify(_dontRelayToTarget).has_key

    # we do not want several methods defined by 'SimpleItem' to
    # be used (because they are stupid: e.g. implement part of the ObjectManager
    # API, while we are not ObjectManagers)
    # We tried not to derive from "SimpleItem", but other Zope part
    # rely on this broken behaviour.
    _dontRelayToReference= (
        'objectIds', 'objectValues', 'objectItems',
        'this',
        'tpURL', 'tpValues',
        )
    _dontRelayToReference= _dictify(_dontRelayToReference).has_key

    _inherited__of__ = SimpleItem.__of__

    def __of__(self, parent):
        # DM: Acquisition is a really interesting thing!
        #     when "__of__" is called for the first time, "parent" is
        #     still unwrapped and "restrictedTraverse" will fail
        #     therefore, we check for it and return "self" in this case
        #     Usually, we will be called a second time, and this time
        #     "parent" is wrapped and we return the result.
        if not hasattr(parent,'aq_base'): return self
        try:
            self._v_recursion+= 1
            if self._v_recursion >= self._max_recursion:
                raise SystemError('Excessive recursion')
            try:
                ob = parent.restrictedTraverse(self.targetPath)
                return _Proxy(self,parent,ob).__of__(parent)
            except:
                if self._v_recursion > 1: raise
                # does not work
                # -- a bug in "ExtensionClass"
                # "PMethod"s and "CMethod"s are incompatible -- corresponding
                # bug report was wrongfully rejected
                #return Reference.inheritedAttribute('__of__')(self,parent)
                return self._inherited__of__(parent)
        finally:
            self._v_recursion-= 1

    # work around an apparent bug in Five as delivered with Zope 2.9
    #   (reported by J Cameron Cooper: symptom TALES path expressions
    #   cannot locate target attributes (and fail with a "LookupException")
    # It has turned out that this has not been a problem with Five
    #   but has the following cause:
    #   the traversal methods are resolved as "Reference" methods and
    #   consequently, their "path" is resolved with respect to the
    #   reference without taking the 'target' into account.
    #   The "__bobo_traverse__" below fixes this again -- turning
    #   the traversal methods effectively into proxy methods.
    #   An alternative would be to implement the traversal methods
    #   explicitely as proxy methods.
    # Because '__bobo_traverse__' triggers weaknesses in the security
    #   checks during traversal when elementary values are returned,
    #   we implement the alternative.
##    def __bobo_traverse__(self, request, name):         
##        proxy = aq_base(self).__of__(aq_parent(self))
##        return getattr(proxy, name)

InitializeClass(Reference)


class _Proxy(Implicit):
    '''auxiliary lookup class.'''
    def __init__(self,reference,parent,target):
        # print '_Proxy.__init__: dict', id(self.__dict__)
        self.__reference= reference
        self.__wrappedReference= Implicit.__of__(reference,parent)
        self.__target= target
        # see whether we want to have a "__call__" method
        #   this no longer works due to Python changes
        ## if hasattr(target,'__call__'): self.__call__= self.__call

    # because Python no longer resolves '__XXX__' methods from the instance
    #  we need to define this and cannot rely on the general method
    #  handling
    def __call__(self,*args,**kw):
        '''call *target*.__call__ with the correct context.

        ATT: the acquisition context is only partially correct.
             At least, "aq_parent" is correct which is essential for
             instances of 'Shared.DC.Scripts.Bindings'.
        '''
        # avoid acquisition
        d = self.__dict__
        wrappedReference= d['_Proxy__wrappedReference']
        target= d['_Proxy__target']
        return apply(target.__of__(wrappedReference.aq_parent).__call__,args,kw)

    def __getattr__(self,attr):
        d= self.__dict__
        reference= d['_Proxy__reference']
        # try to make "cut&paste" work
        # will not work, because "OFS.CopySupport.manage_pasteObjects"
        # calls "Acquisition.aq_base" and it cannot be customized
        # be definitions in our class
        #if attr == 'aq_base': return reference.aq_base
        # we are not an acquisition wrapper; thus, refuse to serve "aq_"
        if attr.startswith('aq_'): raise AttributeError, attr
        # avoid acquisition
        wrappedReference= d['_Proxy__wrappedReference']
        target= d['_Proxy__target']
        if not reference._dontRelayToReference(attr) \
           and hasattr(reference,attr):
            return getattr(wrappedReference,attr)
        if reference._dontRelayToTarget(attr):
            raise AttributeError, attr
        r= getattr(target,attr)
        if type(r) is PythonMethodType and isinstance(r.im_self, Base):
            # an 'ExtensionClass' instance method: special
            #  wrapping trickery may be necessary to get the
            #  acquisition context right.
            return _MethodProxy(r,attr,r.im_self,self)
        return r

    def cb_isMoveable(self):
        # we cannot be moved because "OFS.CopySupport.manage_pasteObjects"
        # does not provide a hook to go back from the proxy to the true
        # reference
        # workaround: use "copy" followed by "delete"
        return 0

    def _getCopy(self,dest):
        '''get a copy of *self* for use in *dest*.
        Ensure, we copy the reference and not the proxy.'''
        # avoid acquisition
        d= self.__dict__
        return d['_Proxy__reference']._getCopy(dest)

    # implement traversal methods; see above for motivation
    restrictedTraverse = Traversable.restrictedTraverse.im_func
    unrestrictedTraverse = Traversable.unrestrictedTraverse.im_func


class _MethodProxy(Base):
    '''Acquisition treats Python Methods specially. Their 'im_self' does not
    get full acquisition context but only a restricted one.
    The mechanism is thus, that it breaks down altogether for methods looked
    up through '_Proxy' instances.

    This class tries to keep the acquisition context as long as possible
    and only uses it when the method is called.
    ATT: it is very likely, that it will break at some places.
    '''
    def __init__(self,method,name,obj,ref):
        self.__method= method
        self.__name= name
        self.__ref= ref
        self.im_self= obj

    def __getattr__(self,attr):
        # avoid acquisition
        d= self.__dict__
        method= d['_MethodProxy__method']
        return getattr(method,attr)

    def __of__(self,parent):
        # we emulate the usual special handling
        # for Python Methods. We try to get at least Python Scripts
        # and other classes derived from "Shared.DC.Scripts.Binding.Binding"
        # happy
        if aq_base(parent) is parent:
            # not yet wrapped, ignore
            return self
        # avoid acquisition
        d= self.__dict__
        ref= d['_MethodProxy__ref']
        if ref is parent.aq_self:
            context= parent.aq_parent
            return _MethodProxy(d['_MethodProxy__method'],
                                d['_MethodProxy__name'],
                                d['im_self'].__of__(context),
                                parent)
        return self

    def __call__(self,*args,**kw):
        '''call the method'''
        # avoid acquisition
        d= self.__dict__
        method= d['_MethodProxy__method']
        im_self= d['im_self']
        m= getattr(method.im_class,self.__name)
        return apply(m,(im_self,) + args,kw)

