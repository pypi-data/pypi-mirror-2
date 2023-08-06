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

class Measurement(IdentifiedObject):
    """A Measurement represents any measured, calculated or non-measured non-calculated quantity. Any piece of equipment may contain Measurements, e.g. a substation may have temperature measurements and door open indications, a transformer may have oil temperature and tank pressure measurements, a bay may contain a number of power flow measurements and a Breaker may contain a switch status measurement.  The PSR - Measurement association is intended to capture this use of Measurement and is included in the naming hierarchy based on EquipmentContainer. The naming hierarchy typically has Measurements as leafs, e.g. Substation-VoltageLevel-Bay-Switch-Measurement. Some Measurements represent quantities related to a particular sensor location in the network, e.g. a voltage transformer (PT) at a busbar or a current transformer (CT) at the bar between a breaker and an isolator. The sensing position is not captured in the PSR - Measurement association. Instead it is captured by the Measurement - Terminal association that is used to define the sensing location in the network topology. The location is defined by the connection of the Terminal to ConductingEquipment.  Two possible paths exist: 1) Measurement-Terminal- ConnectivityNode-Terminal-ConductingEquipment 2) Measurement-Terminal-ConductingEquipment Alternative 2 is the only allowed use.  When the sensor location is needed both Measurement-PSR and Measurement-Terminal are used. The Measurement-Terminal association is never used alone.
    """

    def __init__(self, measurementType='', PowerSystemResource=None, Locations=None, Terminal=None, Unit=None, tieToMeasurement0=None, Asset=None, Documents=None, *args, **kw_args):
        """Initialises a new 'Measurement' instance.

        @param measurementType: Specifies the type of Measurement, e.g. IndoorTemperature, OutDoorTemperature, BusVoltage, GeneratorVoltage, LineFlow etc. 
        @param PowerSystemResource: The PowerSystemResource that contains the Measurement in the naming hierarchy
        @param Locations:
        @param Terminal: One or more measurements may be associated with a terminal in the network
        @param Unit: The Unit for the Measurement
        @param tieToMeasurement0:
        @param Asset:
        @param Documents: Measurements are specified in types of documents, such as procedures.
        """
        #: Specifies the type of Measurement, e.g. IndoorTemperature, OutDoorTemperature, BusVoltage, GeneratorVoltage, LineFlow etc.
        self.measurementType = measurementType

        self._PowerSystemResource = None
        self.PowerSystemResource = PowerSystemResource

        self._Locations = []
        self.Locations = [] if Locations is None else Locations

        self._Terminal = None
        self.Terminal = Terminal

        self._Unit = None
        self.Unit = Unit

        self._tieToMeasurement0 = []
        self.tieToMeasurement0 = [] if tieToMeasurement0 is None else tieToMeasurement0

        self._Asset = None
        self.Asset = Asset

        self._Documents = []
        self.Documents = [] if Documents is None else Documents

        super(Measurement, self).__init__(*args, **kw_args)

    _attrs = ["measurementType"]
    _attr_types = {"measurementType": str}
    _defaults = {"measurementType": ''}
    _enums = {}
    _refs = ["PowerSystemResource", "Locations", "Terminal", "Unit", "tieToMeasurement0", "Asset", "Documents"]
    _many_refs = ["Locations", "tieToMeasurement0", "Documents"]

    def getPowerSystemResource(self):
        """The PowerSystemResource that contains the Measurement in the naming hierarchy
        """
        return self._PowerSystemResource

    def setPowerSystemResource(self, value):
        if self._PowerSystemResource is not None:
            filtered = [x for x in self.PowerSystemResource.Measurements if x != self]
            self._PowerSystemResource._Measurements = filtered

        self._PowerSystemResource = value
        if self._PowerSystemResource is not None:
            if self not in self._PowerSystemResource._Measurements:
                self._PowerSystemResource._Measurements.append(self)

    PowerSystemResource = property(getPowerSystemResource, setPowerSystemResource)

    def getLocations(self):
        
        return self._Locations

    def setLocations(self, value):
        for p in self._Locations:
            filtered = [q for q in p.Measurements if q != self]
            self._Locations._Measurements = filtered
        for r in value:
            if self not in r._Measurements:
                r._Measurements.append(self)
        self._Locations = value

    Locations = property(getLocations, setLocations)

    def addLocations(self, *Locations):
        for obj in Locations:
            if self not in obj._Measurements:
                obj._Measurements.append(self)
            self._Locations.append(obj)

    def removeLocations(self, *Locations):
        for obj in Locations:
            if self in obj._Measurements:
                obj._Measurements.remove(self)
            self._Locations.remove(obj)

    def getTerminal(self):
        """One or more measurements may be associated with a terminal in the network
        """
        return self._Terminal

    def setTerminal(self, value):
        if self._Terminal is not None:
            filtered = [x for x in self.Terminal.Measurements if x != self]
            self._Terminal._Measurements = filtered

        self._Terminal = value
        if self._Terminal is not None:
            if self not in self._Terminal._Measurements:
                self._Terminal._Measurements.append(self)

    Terminal = property(getTerminal, setTerminal)

    def getUnit(self):
        """The Unit for the Measurement
        """
        return self._Unit

    def setUnit(self, value):
        if self._Unit is not None:
            filtered = [x for x in self.Unit.Measurements if x != self]
            self._Unit._Measurements = filtered

        self._Unit = value
        if self._Unit is not None:
            if self not in self._Unit._Measurements:
                self._Unit._Measurements.append(self)

    Unit = property(getUnit, setUnit)

    def gettieToMeasurement0(self):
        
        return self._tieToMeasurement0

    def settieToMeasurement0(self, value):
        for x in self._tieToMeasurement0:
            x.measurement0 = None
        for y in value:
            y._measurement0 = self
        self._tieToMeasurement0 = value

    tieToMeasurement0 = property(gettieToMeasurement0, settieToMeasurement0)

    def addtieToMeasurement0(self, *tieToMeasurement0):
        for obj in tieToMeasurement0:
            obj.measurement0 = self

    def removetieToMeasurement0(self, *tieToMeasurement0):
        for obj in tieToMeasurement0:
            obj.measurement0 = None

    def getAsset(self):
        
        return self._Asset

    def setAsset(self, value):
        if self._Asset is not None:
            filtered = [x for x in self.Asset.Measurements if x != self]
            self._Asset._Measurements = filtered

        self._Asset = value
        if self._Asset is not None:
            if self not in self._Asset._Measurements:
                self._Asset._Measurements.append(self)

    Asset = property(getAsset, setAsset)

    def getDocuments(self):
        """Measurements are specified in types of documents, such as procedures.
        """
        return self._Documents

    def setDocuments(self, value):
        for p in self._Documents:
            filtered = [q for q in p.Measurements if q != self]
            self._Documents._Measurements = filtered
        for r in value:
            if self not in r._Measurements:
                r._Measurements.append(self)
        self._Documents = value

    Documents = property(getDocuments, setDocuments)

    def addDocuments(self, *Documents):
        for obj in Documents:
            if self not in obj._Measurements:
                obj._Measurements.append(self)
            self._Documents.append(obj)

    def removeDocuments(self, *Documents):
        for obj in Documents:
            if self in obj._Measurements:
                obj._Measurements.remove(self)
            self._Documents.remove(obj)

