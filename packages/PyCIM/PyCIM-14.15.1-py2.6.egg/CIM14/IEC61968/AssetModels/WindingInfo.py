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

class WindingInfo(IdentifiedObject):
    """Winding data.
    """

    def __init__(self, connectionKind="Yn", r=0.0, phaseAngle=0, emergencyS=0.0, ratedU=0.0, insulationU=0.0, ratedS=0.0, sequenceNumber=0, shortTermS=0.0, Windings=None, WindingTests=None, TransformerInfo=None, ToWindingSpecs=None, *args, **kw_args):
        """Initialises a new 'WindingInfo' instance.

        @param connectionKind: Kind of connection of this winding. Values are: "Yn", "Y", "D", "I", "Z", "A", "Zn"
        @param r: DC resistance of this winding. 
        @param phaseAngle: Winding phase angle where 360 degrees are represented with clock hours, so the valid values are {0, ..., 11}. For example, to express winding code 'Dyn11', set attributes as follows: 'connectionKind' = Yn and 'phaseAngle' = 11. 
        @param emergencyS: Apparent power that the winding can carry under emergency conditions. 
        @param ratedU: Rated voltage of this winding: phase-phase for three-phase windings, and either phase-phase or phase-neutral for single-phase windings. 
        @param insulationU: Basic insulation level voltage rating. 
        @param ratedS: Normal apparent power rating of this winding. 
        @param sequenceNumber: Sequence number for this winding, corresponding to the winding's order in the TransformerBank.vectorGroup attribute. Highest voltage winding should be '1'. 
        @param shortTermS: Apparent power that this winding can carry for a short period of time. 
        @param Windings: All windings described by this winding data.
        @param WindingTests: All winding tests during which voltage or current was applied to this winding.
        @param TransformerInfo: Transformer data that this winding description is part of.
        @param ToWindingSpecs: Tap steps and induced voltage/angle measurements for tests in which this winding was not excited.
        """
        #: Kind of connection of this winding. Values are: "Yn", "Y", "D", "I", "Z", "A", "Zn"
        self.connectionKind = connectionKind

        #: DC resistance of this winding.
        self.r = r

        #: Winding phase angle where 360 degrees are represented with clock hours, so the valid values are {0, ..., 11}. For example, to express winding code 'Dyn11', set attributes as follows: 'connectionKind' = Yn and 'phaseAngle' = 11.
        self.phaseAngle = phaseAngle

        #: Apparent power that the winding can carry under emergency conditions.
        self.emergencyS = emergencyS

        #: Rated voltage of this winding: phase-phase for three-phase windings, and either phase-phase or phase-neutral for single-phase windings.
        self.ratedU = ratedU

        #: Basic insulation level voltage rating.
        self.insulationU = insulationU

        #: Normal apparent power rating of this winding.
        self.ratedS = ratedS

        #: Sequence number for this winding, corresponding to the winding's order in the TransformerBank.vectorGroup attribute. Highest voltage winding should be '1'.
        self.sequenceNumber = sequenceNumber

        #: Apparent power that this winding can carry for a short period of time.
        self.shortTermS = shortTermS

        self._Windings = []
        self.Windings = [] if Windings is None else Windings

        self._WindingTests = []
        self.WindingTests = [] if WindingTests is None else WindingTests

        self._TransformerInfo = None
        self.TransformerInfo = TransformerInfo

        self._ToWindingSpecs = []
        self.ToWindingSpecs = [] if ToWindingSpecs is None else ToWindingSpecs

        super(WindingInfo, self).__init__(*args, **kw_args)

    _attrs = ["connectionKind", "r", "phaseAngle", "emergencyS", "ratedU", "insulationU", "ratedS", "sequenceNumber", "shortTermS"]
    _attr_types = {"connectionKind": str, "r": float, "phaseAngle": int, "emergencyS": float, "ratedU": float, "insulationU": float, "ratedS": float, "sequenceNumber": int, "shortTermS": float}
    _defaults = {"connectionKind": "Yn", "r": 0.0, "phaseAngle": 0, "emergencyS": 0.0, "ratedU": 0.0, "insulationU": 0.0, "ratedS": 0.0, "sequenceNumber": 0, "shortTermS": 0.0}
    _enums = {"connectionKind": "WindingConnection"}
    _refs = ["Windings", "WindingTests", "TransformerInfo", "ToWindingSpecs"]
    _many_refs = ["Windings", "WindingTests", "ToWindingSpecs"]

    def getWindings(self):
        """All windings described by this winding data.
        """
        return self._Windings

    def setWindings(self, value):
        for x in self._Windings:
            x._WindingInfo = None
        for y in value:
            y._WindingInfo = self
        self._Windings = value

    Windings = property(getWindings, setWindings)

    def addWindings(self, *Windings):
        for obj in Windings:
            obj._WindingInfo = self
            self._Windings.append(obj)

    def removeWindings(self, *Windings):
        for obj in Windings:
            obj._WindingInfo = None
            self._Windings.remove(obj)

    def getWindingTests(self):
        """All winding tests during which voltage or current was applied to this winding.
        """
        return self._WindingTests

    def setWindingTests(self, value):
        for x in self._WindingTests:
            x._FromWinding = None
        for y in value:
            y._FromWinding = self
        self._WindingTests = value

    WindingTests = property(getWindingTests, setWindingTests)

    def addWindingTests(self, *WindingTests):
        for obj in WindingTests:
            obj._FromWinding = self
            self._WindingTests.append(obj)

    def removeWindingTests(self, *WindingTests):
        for obj in WindingTests:
            obj._FromWinding = None
            self._WindingTests.remove(obj)

    def getTransformerInfo(self):
        """Transformer data that this winding description is part of.
        """
        return self._TransformerInfo

    def setTransformerInfo(self, value):
        if self._TransformerInfo is not None:
            filtered = [x for x in self.TransformerInfo.WindingInfos if x != self]
            self._TransformerInfo._WindingInfos = filtered

        self._TransformerInfo = value
        if self._TransformerInfo is not None:
            self._TransformerInfo._WindingInfos.append(self)

    TransformerInfo = property(getTransformerInfo, setTransformerInfo)

    def getToWindingSpecs(self):
        """Tap steps and induced voltage/angle measurements for tests in which this winding was not excited.
        """
        return self._ToWindingSpecs

    def setToWindingSpecs(self, value):
        for x in self._ToWindingSpecs:
            x._ToWinding = None
        for y in value:
            y._ToWinding = self
        self._ToWindingSpecs = value

    ToWindingSpecs = property(getToWindingSpecs, setToWindingSpecs)

    def addToWindingSpecs(self, *ToWindingSpecs):
        for obj in ToWindingSpecs:
            obj._ToWinding = self
            self._ToWindingSpecs.append(obj)

    def removeToWindingSpecs(self, *ToWindingSpecs):
        for obj in ToWindingSpecs:
            obj._ToWinding = None
            self._ToWindingSpecs.remove(obj)

