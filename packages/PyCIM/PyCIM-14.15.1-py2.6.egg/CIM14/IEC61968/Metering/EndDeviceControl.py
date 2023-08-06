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

class EndDeviceControl(IdentifiedObject):
    """Instructs an EndDeviceAsset (or EndDeviceGroup) to perform a specified action.
    """

    def __init__(self, type='', drProgramMandatory=False, priceSignal=0.0, drProgramLevel=0, EndDeviceGroup=None, DemandResponseProgram=None, CustomerAgreement=None, EndDeviceAsset=None, scheduledInterval=None, *args, **kw_args):
        """Initialises a new 'EndDeviceControl' instance.

        @param type: Type of control. 
        @param drProgramMandatory: Whether a demand response program request is mandatory. Note: Attribute is not defined on DemandResponseProgram as it is not its inherent property (it serves to control it). 
        @param priceSignal: (if applicable) Price signal used as parameter for this end device control. 
        @param drProgramLevel: Level of a demand response program request, where 0=emergency. Note: Attribute is not defined on DemandResponseProgram as it is not its inherent property (it serves to control it). 
        @param EndDeviceGroup: End device group receiving commands from this end device control.
        @param DemandResponseProgram: Demand response program for this end device control.
        @param CustomerAgreement: Could be deprecated in the future.
        @param EndDeviceAsset: End device asset receiving commands from this end device control.
        @param scheduledInterval: (if control has scheduled duration) Date and time interval the control has been scheduled to execute within.
        """
        #: Type of control.
        self.type = type

        #: Whether a demand response program request is mandatory. Note: Attribute is not defined on DemandResponseProgram as it is not its inherent property (it serves to control it).
        self.drProgramMandatory = drProgramMandatory

        #: (if applicable) Price signal used as parameter for this end device control.
        self.priceSignal = priceSignal

        #: Level of a demand response program request, where 0=emergency. Note: Attribute is not defined on DemandResponseProgram as it is not its inherent property (it serves to control it).
        self.drProgramLevel = drProgramLevel

        self._EndDeviceGroup = None
        self.EndDeviceGroup = EndDeviceGroup

        self._DemandResponseProgram = None
        self.DemandResponseProgram = DemandResponseProgram

        self._CustomerAgreement = None
        self.CustomerAgreement = CustomerAgreement

        self._EndDeviceAsset = None
        self.EndDeviceAsset = EndDeviceAsset

        self.scheduledInterval = scheduledInterval

        super(EndDeviceControl, self).__init__(*args, **kw_args)

    _attrs = ["type", "drProgramMandatory", "priceSignal", "drProgramLevel"]
    _attr_types = {"type": str, "drProgramMandatory": bool, "priceSignal": float, "drProgramLevel": int}
    _defaults = {"type": '', "drProgramMandatory": False, "priceSignal": 0.0, "drProgramLevel": 0}
    _enums = {}
    _refs = ["EndDeviceGroup", "DemandResponseProgram", "CustomerAgreement", "EndDeviceAsset", "scheduledInterval"]
    _many_refs = []

    def getEndDeviceGroup(self):
        """End device group receiving commands from this end device control.
        """
        return self._EndDeviceGroup

    def setEndDeviceGroup(self, value):
        if self._EndDeviceGroup is not None:
            filtered = [x for x in self.EndDeviceGroup.EndDeviceControls if x != self]
            self._EndDeviceGroup._EndDeviceControls = filtered

        self._EndDeviceGroup = value
        if self._EndDeviceGroup is not None:
            self._EndDeviceGroup._EndDeviceControls.append(self)

    EndDeviceGroup = property(getEndDeviceGroup, setEndDeviceGroup)

    def getDemandResponseProgram(self):
        """Demand response program for this end device control.
        """
        return self._DemandResponseProgram

    def setDemandResponseProgram(self, value):
        if self._DemandResponseProgram is not None:
            filtered = [x for x in self.DemandResponseProgram.EndDeviceControls if x != self]
            self._DemandResponseProgram._EndDeviceControls = filtered

        self._DemandResponseProgram = value
        if self._DemandResponseProgram is not None:
            self._DemandResponseProgram._EndDeviceControls.append(self)

    DemandResponseProgram = property(getDemandResponseProgram, setDemandResponseProgram)

    def getCustomerAgreement(self):
        """Could be deprecated in the future.
        """
        return self._CustomerAgreement

    def setCustomerAgreement(self, value):
        if self._CustomerAgreement is not None:
            filtered = [x for x in self.CustomerAgreement.EndDeviceControls if x != self]
            self._CustomerAgreement._EndDeviceControls = filtered

        self._CustomerAgreement = value
        if self._CustomerAgreement is not None:
            self._CustomerAgreement._EndDeviceControls.append(self)

    CustomerAgreement = property(getCustomerAgreement, setCustomerAgreement)

    def getEndDeviceAsset(self):
        """End device asset receiving commands from this end device control.
        """
        return self._EndDeviceAsset

    def setEndDeviceAsset(self, value):
        if self._EndDeviceAsset is not None:
            filtered = [x for x in self.EndDeviceAsset.EndDeviceControls if x != self]
            self._EndDeviceAsset._EndDeviceControls = filtered

        self._EndDeviceAsset = value
        if self._EndDeviceAsset is not None:
            self._EndDeviceAsset._EndDeviceControls.append(self)

    EndDeviceAsset = property(getEndDeviceAsset, setEndDeviceAsset)

    # (if control has scheduled duration) Date and time interval the control has been scheduled to execute within.
    scheduledInterval = None

