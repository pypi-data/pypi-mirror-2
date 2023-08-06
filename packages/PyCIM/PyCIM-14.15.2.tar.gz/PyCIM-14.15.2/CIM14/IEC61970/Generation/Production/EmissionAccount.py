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

from CIM14.IEC61970.Core.Curve import Curve

class EmissionAccount(Curve):
    """Accounts for tracking emissions usage and credits for thermal generating units. A unit may have zero or more emission accounts, and will typically have one for tracking usage and one for tracking credits.
    """

    def __init__(self, emissionType="chlorine", emissionValueSource="measured", ThermalGeneratingUnit=None, *args, **kw_args):
        """Initialises a new 'EmissionAccount' instance.

        @param emissionType: The type of emission, for example sulfur dioxide (SO2). The y1AxisUnits of the curve contains the unit of measure (e.g. kg) and the emissionType is the type of emission (e.g. sulfer dioxide). Values are: "chlorine", "carbonDioxide", "hydrogenSulfide", "nitrogenOxide", "sulfurDioxide", "carbonDisulfide"
        @param emissionValueSource: The source of the emission value. Values are: "measured", "calculated"
        @param ThermalGeneratingUnit: A thermal generating unit may have one or more emission allowance accounts
        """
        #: The type of emission, for example sulfur dioxide (SO2). The y1AxisUnits of the curve contains the unit of measure (e.g. kg) and the emissionType is the type of emission (e.g. sulfer dioxide). Values are: "chlorine", "carbonDioxide", "hydrogenSulfide", "nitrogenOxide", "sulfurDioxide", "carbonDisulfide"
        self.emissionType = emissionType

        #: The source of the emission value. Values are: "measured", "calculated"
        self.emissionValueSource = emissionValueSource

        self._ThermalGeneratingUnit = None
        self.ThermalGeneratingUnit = ThermalGeneratingUnit

        super(EmissionAccount, self).__init__(*args, **kw_args)

    _attrs = ["emissionType", "emissionValueSource"]
    _attr_types = {"emissionType": str, "emissionValueSource": str}
    _defaults = {"emissionType": "chlorine", "emissionValueSource": "measured"}
    _enums = {"emissionType": "EmissionType", "emissionValueSource": "EmissionValueSource"}
    _refs = ["ThermalGeneratingUnit"]
    _many_refs = []

    def getThermalGeneratingUnit(self):
        """A thermal generating unit may have one or more emission allowance accounts
        """
        return self._ThermalGeneratingUnit

    def setThermalGeneratingUnit(self, value):
        if self._ThermalGeneratingUnit is not None:
            filtered = [x for x in self.ThermalGeneratingUnit.EmmissionAccounts if x != self]
            self._ThermalGeneratingUnit._EmmissionAccounts = filtered

        self._ThermalGeneratingUnit = value
        if self._ThermalGeneratingUnit is not None:
            if self not in self._ThermalGeneratingUnit._EmmissionAccounts:
                self._ThermalGeneratingUnit._EmmissionAccounts.append(self)

    ThermalGeneratingUnit = property(getThermalGeneratingUnit, setThermalGeneratingUnit)

