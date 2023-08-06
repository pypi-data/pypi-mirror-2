# Copyright (C) 2010-2011 Richard Lincoln
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from CIM14.IEC61970.Core.IdentifiedObject import IdentifiedObject

class MetaBlockConnectable(IdentifiedObject):
    """This is a source connection for a block input at the dynamics meta-data level.   The subtypes represent different ways to obtain the numbers.  Note that a block output is NOT derived from this class since block outputs can only be computed from references to other blocks via the BlockOutputReference class.
    """

    def __init__(self, StandardControlBlock_MetaBlockStateReference=None, MetaBlockOutputReference=None, MetaBlockStateReference=None, BlockInputReference=None, StandardControlBlock_MetaBlockInputReference=None, StandardControlBlock_MetaBlockParameterReference=None, MetaBlockParameterReference=None, StandardControlBlock_MetaBlockOutputReference=None, MetaBlockInputReference=None, *args, **kw_args):
        """Initialises a new 'MetaBlockConnectable' instance.

        @param StandardControlBlock_MetaBlockStateReference:
        @param MetaBlockOutputReference:
        @param MetaBlockStateReference:
        @param BlockInputReference: Each block reference input is usually tied to one (sometimes zero for optional inputs) external block inputs or internal block reference outputs.
        @param StandardControlBlock_MetaBlockInputReference:
        @param StandardControlBlock_MetaBlockParameterReference:
        @param MetaBlockParameterReference:
        @param StandardControlBlock_MetaBlockOutputReference:
        @param MetaBlockInputReference:
        """
        self._StandardControlBlock_MetaBlockStateReference = []
        self.StandardControlBlock_MetaBlockStateReference = [] if StandardControlBlock_MetaBlockStateReference is None else StandardControlBlock_MetaBlockStateReference

        self._MetaBlockOutputReference = []
        self.MetaBlockOutputReference = [] if MetaBlockOutputReference is None else MetaBlockOutputReference

        self._MetaBlockStateReference = []
        self.MetaBlockStateReference = [] if MetaBlockStateReference is None else MetaBlockStateReference

        self._BlockInputReference = []
        self.BlockInputReference = [] if BlockInputReference is None else BlockInputReference

        self._StandardControlBlock_MetaBlockInputReference = []
        self.StandardControlBlock_MetaBlockInputReference = [] if StandardControlBlock_MetaBlockInputReference is None else StandardControlBlock_MetaBlockInputReference

        self._StandardControlBlock_MetaBlockParameterReference = []
        self.StandardControlBlock_MetaBlockParameterReference = [] if StandardControlBlock_MetaBlockParameterReference is None else StandardControlBlock_MetaBlockParameterReference

        self._MetaBlockParameterReference = []
        self.MetaBlockParameterReference = [] if MetaBlockParameterReference is None else MetaBlockParameterReference

        self._StandardControlBlock_MetaBlockOutputReference = []
        self.StandardControlBlock_MetaBlockOutputReference = [] if StandardControlBlock_MetaBlockOutputReference is None else StandardControlBlock_MetaBlockOutputReference

        self._MetaBlockInputReference = []
        self.MetaBlockInputReference = [] if MetaBlockInputReference is None else MetaBlockInputReference

        super(MetaBlockConnectable, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["StandardControlBlock_MetaBlockStateReference", "MetaBlockOutputReference", "MetaBlockStateReference", "BlockInputReference", "StandardControlBlock_MetaBlockInputReference", "StandardControlBlock_MetaBlockParameterReference", "MetaBlockParameterReference", "StandardControlBlock_MetaBlockOutputReference", "MetaBlockInputReference"]
    _many_refs = ["StandardControlBlock_MetaBlockStateReference", "MetaBlockOutputReference", "MetaBlockStateReference", "BlockInputReference", "StandardControlBlock_MetaBlockInputReference", "StandardControlBlock_MetaBlockParameterReference", "MetaBlockParameterReference", "StandardControlBlock_MetaBlockOutputReference", "MetaBlockInputReference"]

    def getStandardControlBlock_MetaBlockStateReference(self):
        
        return self._StandardControlBlock_MetaBlockStateReference

    def setStandardControlBlock_MetaBlockStateReference(self, value):
        for x in self._StandardControlBlock_MetaBlockStateReference:
            x.StandardControlBlock_MetaBlockConnectable = None
        for y in value:
            y._StandardControlBlock_MetaBlockConnectable = self
        self._StandardControlBlock_MetaBlockStateReference = value

    StandardControlBlock_MetaBlockStateReference = property(getStandardControlBlock_MetaBlockStateReference, setStandardControlBlock_MetaBlockStateReference)

    def addStandardControlBlock_MetaBlockStateReference(self, *StandardControlBlock_MetaBlockStateReference):
        for obj in StandardControlBlock_MetaBlockStateReference:
            obj.StandardControlBlock_MetaBlockConnectable = self

    def removeStandardControlBlock_MetaBlockStateReference(self, *StandardControlBlock_MetaBlockStateReference):
        for obj in StandardControlBlock_MetaBlockStateReference:
            obj.StandardControlBlock_MetaBlockConnectable = None

    def getMetaBlockOutputReference(self):
        
        return self._MetaBlockOutputReference

    def setMetaBlockOutputReference(self, value):
        for x in self._MetaBlockOutputReference:
            x.MetaBlockConnectable = None
        for y in value:
            y._MetaBlockConnectable = self
        self._MetaBlockOutputReference = value

    MetaBlockOutputReference = property(getMetaBlockOutputReference, setMetaBlockOutputReference)

    def addMetaBlockOutputReference(self, *MetaBlockOutputReference):
        for obj in MetaBlockOutputReference:
            obj.MetaBlockConnectable = self

    def removeMetaBlockOutputReference(self, *MetaBlockOutputReference):
        for obj in MetaBlockOutputReference:
            obj.MetaBlockConnectable = None

    def getMetaBlockStateReference(self):
        
        return self._MetaBlockStateReference

    def setMetaBlockStateReference(self, value):
        for x in self._MetaBlockStateReference:
            x.MetaBlockConnectable = None
        for y in value:
            y._MetaBlockConnectable = self
        self._MetaBlockStateReference = value

    MetaBlockStateReference = property(getMetaBlockStateReference, setMetaBlockStateReference)

    def addMetaBlockStateReference(self, *MetaBlockStateReference):
        for obj in MetaBlockStateReference:
            obj.MetaBlockConnectable = self

    def removeMetaBlockStateReference(self, *MetaBlockStateReference):
        for obj in MetaBlockStateReference:
            obj.MetaBlockConnectable = None

    def getBlockInputReference(self):
        """Each block reference input is usually tied to one (sometimes zero for optional inputs) external block inputs or internal block reference outputs.
        """
        return self._BlockInputReference

    def setBlockInputReference(self, value):
        for x in self._BlockInputReference:
            x.BlockConnectable = None
        for y in value:
            y._BlockConnectable = self
        self._BlockInputReference = value

    BlockInputReference = property(getBlockInputReference, setBlockInputReference)

    def addBlockInputReference(self, *BlockInputReference):
        for obj in BlockInputReference:
            obj.BlockConnectable = self

    def removeBlockInputReference(self, *BlockInputReference):
        for obj in BlockInputReference:
            obj.BlockConnectable = None

    def getStandardControlBlock_MetaBlockInputReference(self):
        
        return self._StandardControlBlock_MetaBlockInputReference

    def setStandardControlBlock_MetaBlockInputReference(self, value):
        for x in self._StandardControlBlock_MetaBlockInputReference:
            x.StandardControlBlock_MetaBlockConnectable = None
        for y in value:
            y._StandardControlBlock_MetaBlockConnectable = self
        self._StandardControlBlock_MetaBlockInputReference = value

    StandardControlBlock_MetaBlockInputReference = property(getStandardControlBlock_MetaBlockInputReference, setStandardControlBlock_MetaBlockInputReference)

    def addStandardControlBlock_MetaBlockInputReference(self, *StandardControlBlock_MetaBlockInputReference):
        for obj in StandardControlBlock_MetaBlockInputReference:
            obj.StandardControlBlock_MetaBlockConnectable = self

    def removeStandardControlBlock_MetaBlockInputReference(self, *StandardControlBlock_MetaBlockInputReference):
        for obj in StandardControlBlock_MetaBlockInputReference:
            obj.StandardControlBlock_MetaBlockConnectable = None

    def getStandardControlBlock_MetaBlockParameterReference(self):
        
        return self._StandardControlBlock_MetaBlockParameterReference

    def setStandardControlBlock_MetaBlockParameterReference(self, value):
        for x in self._StandardControlBlock_MetaBlockParameterReference:
            x.StandardControlBlock_MetaBlockConnectable = None
        for y in value:
            y._StandardControlBlock_MetaBlockConnectable = self
        self._StandardControlBlock_MetaBlockParameterReference = value

    StandardControlBlock_MetaBlockParameterReference = property(getStandardControlBlock_MetaBlockParameterReference, setStandardControlBlock_MetaBlockParameterReference)

    def addStandardControlBlock_MetaBlockParameterReference(self, *StandardControlBlock_MetaBlockParameterReference):
        for obj in StandardControlBlock_MetaBlockParameterReference:
            obj.StandardControlBlock_MetaBlockConnectable = self

    def removeStandardControlBlock_MetaBlockParameterReference(self, *StandardControlBlock_MetaBlockParameterReference):
        for obj in StandardControlBlock_MetaBlockParameterReference:
            obj.StandardControlBlock_MetaBlockConnectable = None

    def getMetaBlockParameterReference(self):
        
        return self._MetaBlockParameterReference

    def setMetaBlockParameterReference(self, value):
        for x in self._MetaBlockParameterReference:
            x.MetaBlockConnectable = None
        for y in value:
            y._MetaBlockConnectable = self
        self._MetaBlockParameterReference = value

    MetaBlockParameterReference = property(getMetaBlockParameterReference, setMetaBlockParameterReference)

    def addMetaBlockParameterReference(self, *MetaBlockParameterReference):
        for obj in MetaBlockParameterReference:
            obj.MetaBlockConnectable = self

    def removeMetaBlockParameterReference(self, *MetaBlockParameterReference):
        for obj in MetaBlockParameterReference:
            obj.MetaBlockConnectable = None

    def getStandardControlBlock_MetaBlockOutputReference(self):
        
        return self._StandardControlBlock_MetaBlockOutputReference

    def setStandardControlBlock_MetaBlockOutputReference(self, value):
        for x in self._StandardControlBlock_MetaBlockOutputReference:
            x.StandardControlBlock_MetaBlockConnectable = None
        for y in value:
            y._StandardControlBlock_MetaBlockConnectable = self
        self._StandardControlBlock_MetaBlockOutputReference = value

    StandardControlBlock_MetaBlockOutputReference = property(getStandardControlBlock_MetaBlockOutputReference, setStandardControlBlock_MetaBlockOutputReference)

    def addStandardControlBlock_MetaBlockOutputReference(self, *StandardControlBlock_MetaBlockOutputReference):
        for obj in StandardControlBlock_MetaBlockOutputReference:
            obj.StandardControlBlock_MetaBlockConnectable = self

    def removeStandardControlBlock_MetaBlockOutputReference(self, *StandardControlBlock_MetaBlockOutputReference):
        for obj in StandardControlBlock_MetaBlockOutputReference:
            obj.StandardControlBlock_MetaBlockConnectable = None

    def getMetaBlockInputReference(self):
        
        return self._MetaBlockInputReference

    def setMetaBlockInputReference(self, value):
        for x in self._MetaBlockInputReference:
            x.MetaBlockConnectable = None
        for y in value:
            y._MetaBlockConnectable = self
        self._MetaBlockInputReference = value

    MetaBlockInputReference = property(getMetaBlockInputReference, setMetaBlockInputReference)

    def addMetaBlockInputReference(self, *MetaBlockInputReference):
        for obj in MetaBlockInputReference:
            obj.MetaBlockConnectable = self

    def removeMetaBlockInputReference(self, *MetaBlockInputReference):
        for obj in MetaBlockInputReference:
            obj.MetaBlockConnectable = None

