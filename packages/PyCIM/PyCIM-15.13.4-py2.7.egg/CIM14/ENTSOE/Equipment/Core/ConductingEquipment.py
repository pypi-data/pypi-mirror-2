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

from CIM14.ENTSOE.Equipment.Core.Equipment import Equipment

class ConductingEquipment(Equipment):
    """The parts of the power system that are designed to carry current or that are conductively connected therewith. ConductingEquipment is contained within an EquipmentContainer that may be a Substation, or a VoltageLevel or a Bay within a Substation.
    """

    def __init__(self, Terminals=None, BaseVoltage=None, *args, **kw_args):
        """Initialises a new 'ConductingEquipment' instance.

        @param Terminals: ConductingEquipment has 1 or 2 terminals that may be connected to other ConductingEquipment terminals via ConnectivityNodes
        @param BaseVoltage: Use association to ConductingEquipment only when there is no VoltageLevel container used.For the 2010 ENTSOE IOP, the BaseVoltage association for SeriesCompensator and TransformerWinding is required.
        """
        self._Terminals = []
        self.Terminals = [] if Terminals is None else Terminals

        self._BaseVoltage = None
        self.BaseVoltage = BaseVoltage

        super(ConductingEquipment, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Terminals", "BaseVoltage"]
    _many_refs = ["Terminals"]

    def getTerminals(self):
        """ConductingEquipment has 1 or 2 terminals that may be connected to other ConductingEquipment terminals via ConnectivityNodes
        """
        return self._Terminals

    def setTerminals(self, value):
        for x in self._Terminals:
            x.ConductingEquipment = None
        for y in value:
            y._ConductingEquipment = self
        self._Terminals = value

    Terminals = property(getTerminals, setTerminals)

    def addTerminals(self, *Terminals):
        for obj in Terminals:
            obj.ConductingEquipment = self

    def removeTerminals(self, *Terminals):
        for obj in Terminals:
            obj.ConductingEquipment = None

    def getBaseVoltage(self):
        """Use association to ConductingEquipment only when there is no VoltageLevel container used.For the 2010 ENTSOE IOP, the BaseVoltage association for SeriesCompensator and TransformerWinding is required.
        """
        return self._BaseVoltage

    def setBaseVoltage(self, value):
        if self._BaseVoltage is not None:
            filtered = [x for x in self.BaseVoltage.ConductingEquipment if x != self]
            self._BaseVoltage._ConductingEquipment = filtered

        self._BaseVoltage = value
        if self._BaseVoltage is not None:
            if self not in self._BaseVoltage._ConductingEquipment:
                self._BaseVoltage._ConductingEquipment.append(self)

    BaseVoltage = property(getBaseVoltage, setBaseVoltage)

