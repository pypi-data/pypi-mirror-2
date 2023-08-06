#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

"""
Block Properties:

1. Blocks are indexed components that contain other components (including blocks)

2. Blocks have a global attribute that defines whether construction is deferred.  This 
applies to all components that they contain except blocks.  Blocks contained by other blocks
use their local attribute to determine whether construction is deferred.

NOTE: Blocks do not currently maintain statistics about the sets, parameters, constraints, etc that
they contain, including these components from subblocks.
"""

__all__ = ['Block']

import sys

from plugin import *

from pyutilib.component.core import alias, ExtensionPoint
from pyutilib.misc import Container

from component import Component
from sets import Set, _ProductSet, _SetContainer, _BaseSet
from rangeset import RangeSet
from var import Var
from constraint import Objective, Constraint
from param import Param

from indexed_component import IndexedComponent
try:
    from components import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class Block(IndexedComponent):
    """
    A block in an optimization model.  By default, this defers construction of 
    components until data is loaded.
    """

    alias("Block", "Blocks are indexed components that contain one or more " + \
          "other model components.")

    def __init__(self, *args, **kwargs):
        """Constructor"""
        if 'ctype' in kwargs:
            tkwargs = {'ctype':kwargs['ctype']}
        else:
            tkwargs = {'ctype':Block}
        IndexedComponent.__init__(self, *args, **tkwargs)
        #
        self.name=kwargs.get('name', 'unknown')
        self._defer_construction=True
        self._parent_block = None
        #
        # Define component dictionary: component type -> instance
        #
        self._component={}
        for item in ModelComponentFactory.services():
            self._component[  ModelComponentFactory.get_class(item) ] = {}
        #
        # A list of the declarations, in the order that they are
        # specified.
        #
        self._declarations=OrderedDict()

        # Hack. Right now Block objects assume all attributes derived from
        # Component eventually inherit from NumValue, and so have a domain
        # attribute.
        self.domain = None

    def concrete_mode(self):
        """Configure block to immediately construct components"""
        self._defer_construction=False

    def symbolic_mode(self):
        """Configure block to defer construction of components"""
        self._defer_construction=True

    def components(self, ctype=None):
        """
        Return information about the block components.  If ctype is None, return the dictionary
        that maps {component type -> {name -> instance}}.  Otherwise, return the dictionary
        that maps {name -> instance} for the specified component type.
        """
        if ctype is None:
            return self._component
        if ctype in self._component:
             return self._component[ctype]
        raise KeyError, "Unknown component type: %s" % str(ctype)

    def active_components(self, _ctype=None):
        """
        Returns the active components in this block.  If _ctype is None, return the
        dictionary that maps {component type -> {name -> instance}}.  Otherwise, return
        the dictionary that maps {name -> instance} for the specified component type.
        """
        tmp = {}
        if _ctype is None:
            for ctype in self._component:
                tmp[ctype]={}
        elif _ctype in self._component:
            tmp[_ctype]={}
        else:
            raise KeyError, "Unknown component type: %s" % str(_ctype)
        for ctype in tmp:
            for name in self._component[ctype]:
                comp = self._component[ctype][name]
                if comp.active:
                    tmp[ctype][name] = comp
        if not _ctype is None:
            return tmp[_ctype]
        return tmp

    def _add_temporary_set(self,val):
        if val._index_set is not None:
            ctr=0
            for tset in val._index_set:
                if tset.name == "_unknown_":
                    self._construct_temporary_set(
                      tset,
                      val.name+"_index_"+str(ctr)
                    )
                ctr += 1
            val._index = self._construct_temporary_set(
              val._index_set,
              val.name+"_index"
            )
        if isinstance(val._index,_SetContainer) and \
            val._index.name == "_unknown_":
            self._construct_temporary_set(val._index,val.name+"_index")
        if val.domain is not None and val.domain.name == "_unknown_":
            self._construct_temporary_set(val.domain,val.name+"_domain")

    def _construct_temporary_set(self, obj, name):
        if type(obj) is tuple:
           if len(obj) == 1:                #pragma:nocover
                  raise Exception, "Unexpected temporary set construction"
           else:
                  tobj=_ProductSet(*obj)
                  setattr(self,name,tobj)
                  tobj.virtual=True
                  return tobj
        if isinstance(obj,_BaseSet):
           setattr(self,name,obj)
           return obj

    def _clear_attribute(self,name):
        """
        Cleanup the pre-existing model attribute
        """
        if name in self._declarations:
            self.__dict__[name]=None
            del self._component[ self._declarations[name].type() ][name]
            del self._declarations[name]

    def _setattr_exec(self, name, val):
        self._clear_attribute(name)
        val.name=name
        self._add_temporary_set(val)
        self._component[val.type()][name]=val
        self._declarations[name] = val
        self.__dict__[name]=val

        # Presumably self.model refers to the 'root' Block that will
        # eventually be solved, whereas '_parent_block' refers to the
        # immediate parent.

        # Don't let '_parent_block' attributes trigger recursion
        if isinstance(val, Block):
            self.__dict__["_parent_block"] = self
        else:
            curr = self
            while curr is not None:
                val.model = curr
                curr = self._parent_block
        # self is the top level model if self.model is None; otherwise,
        # self.model is the top level model
        if self.model is not None:
            self.__dict__["model"] = self.model
        else:
            self.__dict__["model"] = self

#         # Need to break infinite loop of attribute setting
#         if isinstance(val, Block) and name != "_parent_block":
#             val._parent_block = self
#         else:
#             curr = self
#             while not curr is None:
#                val.model=curr
#                curr = self._parent_block

        frame = sys._getframe(2)
        locals_ = frame.f_locals
        if getattr(val,'rule',None) is None and val.name+'_rule' in locals_:
            val.rule = locals_[val.name+'_rule']
        if not self._defer_construction:
            val.construct(None)

    def __setattr__(self,name,val):
        """Set attributes"""
        #
        # Set Model Declaration
        #
        if name != "_component" and isinstance(val, Component):
            #
            # If this is a component type, then simply set it
            #
            self._setattr_exec(name,val)
        else:
            #
            # Try to set the value. This may fail if the attribute
            # does not already exist in this model, if the set_value
            # function is not defined, or if a bad value is
            # provided. In the latter case, a ValueError will be
            # thrown, which # we raise. Otherwise, this is an object
            # that we need to set directly.
            #
            try:
                self.__dict__[name].set_value(val)
            except ValueError, e:
                raise
            except Exception, e:
                self.__dict__[name]=val

    def pprint(self, filename=None, ostream=None):
        """
        Print a summary of the model info
        """
        if ostream is None:
           ostream = sys.stdout
        if filename is not None:
           OUTPUT=open(filename,"w")
           self.pprint(ostream=OUTPUT)
           OUTPUT.close()
           return
        if ostream is None:
           ostream = sys.stdout
        #
        # We hard-code the order of the core Pyomo modeling
        # components, to ensure that the output follows the logical order
        # that expected by a user.
        #
        items = [Set, RangeSet, Param, Var, Objective, Constraint, Block]
        for item in ExtensionPoint(IModelComponent):
            if not item in items:
                items.append(item)
        for item in items:
            if not item in self._component:
                continue
            keys = self._component[item].keys()
            keys.sort()
            #
            # NOTE: these conditional checks should not be hard-coded.
            #
            print >>ostream, len(keys), item.__name__+" Declarations"
            for key in keys:
                self._component[item][key].pprint(ostream)
            print >>ostream, ""
        #
        # Model Order
        #
        print >>ostream, len(self._declarations),"Declarations:",
        for name in self._declarations:
          print >>ostream, name,
        print >>ostream, ""

    def display(self, filename=None, ostream=None):
        """
        Print the Pyomo model in a verbose format.
        """
        if filename is not None:
           OUTPUT=open(filename,"w")
           self.display(ostream=OUTPUT)
           OUTPUT.close()
           return
        if ostream is None:
           ostream = sys.stdout
        if self.type() is Block:
            print >>ostream, "Block "+self.name
        else:
            print >>ostream, "Model "+self.name
        #
        print >>ostream, ""
        print >>ostream, "  Variables:"
        VAR = self.active_components(Var)
        if len(VAR) == 0:
            print >>ostream, "    None"
        else:
            for ndx in VAR:
                VAR[ndx].display(prefix="    ",ostream=ostream)
        #
        print >>ostream, ""
        print >>ostream, "  Objectives:"
        OBJ = self.active_components(Objective)
        if len(OBJ) == 0:
            print >>ostream, "    None"
        else:
            for ndx in OBJ:
                OBJ[ndx].display(prefix="    ",ostream=ostream)
        print >>ostream, ""
        #
        CON = self.active_components(Constraint)
        print >>ostream, "  Constraints:"
        if len(CON) == 0:
            print >>ostream, "    None"
        else:
            for ndx in CON:
                CON[ndx].display(prefix="    ",ostream=ostream)

