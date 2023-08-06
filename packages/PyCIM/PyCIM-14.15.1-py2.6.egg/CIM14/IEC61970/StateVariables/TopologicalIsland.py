# Copyright (C) 2010 Richard Lincoln
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA, USA

from CIM14.IEC61970.Core.IdentifiedObject import IdentifiedObject

class TopologicalIsland(IdentifiedObject):
    """An electrically connected subset of the network. Topological islands can change as the current network state changes (i.e. switch or Terminal.connected status changes).
    """

    def __init__(self, TopologicalNodes=None, AngleRef_TopologicalNode=None, *args, **kw_args):
        """Initialises a new 'TopologicalIsland' instance.

        @param TopologicalNodes: A topological node belongs to a topological island
        @param AngleRef_TopologicalNode: The angle reference for the island.   Normally there is one TopologicalNode that is selected as the angle reference for each island.   Other reference schemes exist, so the association is optional.
        """
        self._TopologicalNodes = []
        self.TopologicalNodes = [] if TopologicalNodes is None else TopologicalNodes

        self._AngleRef_TopologicalNode = None
        self.AngleRef_TopologicalNode = AngleRef_TopologicalNode

        super(TopologicalIsland, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["TopologicalNodes", "AngleRef_TopologicalNode"]
    _many_refs = ["TopologicalNodes"]

    def getTopologicalNodes(self):
        """A topological node belongs to a topological island
        """
        return self._TopologicalNodes

    def setTopologicalNodes(self, value):
        for x in self._TopologicalNodes:
            x._TopologicalIsland = None
        for y in value:
            y._TopologicalIsland = self
        self._TopologicalNodes = value

    TopologicalNodes = property(getTopologicalNodes, setTopologicalNodes)

    def addTopologicalNodes(self, *TopologicalNodes):
        for obj in TopologicalNodes:
            obj._TopologicalIsland = self
            self._TopologicalNodes.append(obj)

    def removeTopologicalNodes(self, *TopologicalNodes):
        for obj in TopologicalNodes:
            obj._TopologicalIsland = None
            self._TopologicalNodes.remove(obj)

    def getAngleRef_TopologicalNode(self):
        """The angle reference for the island.   Normally there is one TopologicalNode that is selected as the angle reference for each island.   Other reference schemes exist, so the association is optional.
        """
        return self._AngleRef_TopologicalNode

    def setAngleRef_TopologicalNode(self, value):
        if self._AngleRef_TopologicalNode is not None:
            self._AngleRef_TopologicalNode._AngleRef_TopologicalIsland = None

        self._AngleRef_TopologicalNode = value
        if self._AngleRef_TopologicalNode is not None:
            self._AngleRef_TopologicalNode._AngleRef_TopologicalIsland = self

    AngleRef_TopologicalNode = property(getAngleRef_TopologicalNode, setAngleRef_TopologicalNode)

