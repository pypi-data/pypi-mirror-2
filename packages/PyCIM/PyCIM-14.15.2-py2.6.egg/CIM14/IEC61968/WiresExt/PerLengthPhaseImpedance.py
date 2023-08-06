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

class PerLengthPhaseImpedance(IdentifiedObject):
    """Impedance and admittance parameters per unit length for n-wire unbalanced lines, in matrix form.
    """

    def __init__(self, conductorCount=0, ConductorSegments=None, PhaseImpedanceData=None, *args, **kw_args):
        """Initialises a new 'PerLengthPhaseImpedance' instance.

        @param conductorCount: Number of phase, neutral, and other wires retained. Constrains the number of matrix elements and the phase codes that can be used with this matrix. 
        @param ConductorSegments: All conductor segments described by this phase impedance.
        @param PhaseImpedanceData: All data that belong to this conductor phase impedance.
        """
        #: Number of phase, neutral, and other wires retained. Constrains the number of matrix elements and the phase codes that can be used with this matrix.
        self.conductorCount = conductorCount

        self._ConductorSegments = []
        self.ConductorSegments = [] if ConductorSegments is None else ConductorSegments

        self._PhaseImpedanceData = []
        self.PhaseImpedanceData = [] if PhaseImpedanceData is None else PhaseImpedanceData

        super(PerLengthPhaseImpedance, self).__init__(*args, **kw_args)

    _attrs = ["conductorCount"]
    _attr_types = {"conductorCount": int}
    _defaults = {"conductorCount": 0}
    _enums = {}
    _refs = ["ConductorSegments", "PhaseImpedanceData"]
    _many_refs = ["ConductorSegments", "PhaseImpedanceData"]

    def getConductorSegments(self):
        """All conductor segments described by this phase impedance.
        """
        return self._ConductorSegments

    def setConductorSegments(self, value):
        for x in self._ConductorSegments:
            x.PhaseImpedance = None
        for y in value:
            y._PhaseImpedance = self
        self._ConductorSegments = value

    ConductorSegments = property(getConductorSegments, setConductorSegments)

    def addConductorSegments(self, *ConductorSegments):
        for obj in ConductorSegments:
            obj.PhaseImpedance = self

    def removeConductorSegments(self, *ConductorSegments):
        for obj in ConductorSegments:
            obj.PhaseImpedance = None

    def getPhaseImpedanceData(self):
        """All data that belong to this conductor phase impedance.
        """
        return self._PhaseImpedanceData

    def setPhaseImpedanceData(self, value):
        for x in self._PhaseImpedanceData:
            x.PhaseImpedance = None
        for y in value:
            y._PhaseImpedance = self
        self._PhaseImpedanceData = value

    PhaseImpedanceData = property(getPhaseImpedanceData, setPhaseImpedanceData)

    def addPhaseImpedanceData(self, *PhaseImpedanceData):
        for obj in PhaseImpedanceData:
            obj.PhaseImpedance = self

    def removePhaseImpedanceData(self, *PhaseImpedanceData):
        for obj in PhaseImpedanceData:
            obj.PhaseImpedance = None

