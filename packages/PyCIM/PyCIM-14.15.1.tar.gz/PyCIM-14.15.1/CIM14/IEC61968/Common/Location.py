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

class Location(IdentifiedObject):
    """The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment in time. It is defined with one or more postition points (coordinates) in a given coordinate system.
    """

    def __init__(self, geoInfoReference='', corporateCode='', direction='', category='', PositionPoints=None, PowerSystemResources=None, CoordinateSystems=None, Measurements=None, secondaryAddress=None, Assets=None, phone2=None, electronicAddress=None, phone1=None, mainAddress=None, status=None, *args, **kw_args):
        """Initialises a new 'Location' instance.

        @param geoInfoReference: (if applicable) Reference to geographical information source, often external to the utility. 
        @param corporateCode: Utility-specific code for the location. 
        @param direction: (if applicable) Direction that allows field crews to quickly find a given asset. For a given location, such as a street address, this is the relative direction in which to find the asset. For example, a Streetlight may be located at the 'NW' (northwest) corner of the customer's site, or a ServiceDeliveryPoint may be located on the second floor of an apartment building. 
        @param category: Category by utility's corporate standards and practices, relative to the location itself (e.g., geographical, functional accounting, etc., not a given property that happens to exist at that location). 
        @param PositionPoints: Sequence of position points describing this location.
        @param PowerSystemResources: All power system resources at this location.
        @param CoordinateSystems: All coordinate systems used to describe position points of this location.
        @param Measurements:
        @param secondaryAddress: Secondary address of the location. For example, PO Box address may have different ZIP code than that in the 'mainAddress'.
        @param Assets: All assets at this location.
        @param phone2: Additional phone number.
        @param electronicAddress: Electronic address.
        @param phone1: Phone number.
        @param mainAddress: Main address of the location.
        @param status: Status of this location.
        """
        #: (if applicable) Reference to geographical information source, often external to the utility.
        self.geoInfoReference = geoInfoReference

        #: Utility-specific code for the location.
        self.corporateCode = corporateCode

        #: (if applicable) Direction that allows field crews to quickly find a given asset. For a given location, such as a street address, this is the relative direction in which to find the asset. For example, a Streetlight may be located at the 'NW' (northwest) corner of the customer's site, or a ServiceDeliveryPoint may be located on the second floor of an apartment building.
        self.direction = direction

        #: Category by utility's corporate standards and practices, relative to the location itself (e.g., geographical, functional accounting, etc., not a given property that happens to exist at that location).
        self.category = category

        self._PositionPoints = []
        self.PositionPoints = [] if PositionPoints is None else PositionPoints

        self._PowerSystemResources = []
        self.PowerSystemResources = [] if PowerSystemResources is None else PowerSystemResources

        self._CoordinateSystems = []
        self.CoordinateSystems = [] if CoordinateSystems is None else CoordinateSystems

        self._Measurements = []
        self.Measurements = [] if Measurements is None else Measurements

        self.secondaryAddress = secondaryAddress

        self._Assets = []
        self.Assets = [] if Assets is None else Assets

        self.phone2 = phone2

        self.electronicAddress = electronicAddress

        self.phone1 = phone1

        self.mainAddress = mainAddress

        self.status = status

        super(Location, self).__init__(*args, **kw_args)

    _attrs = ["geoInfoReference", "corporateCode", "direction", "category"]
    _attr_types = {"geoInfoReference": str, "corporateCode": str, "direction": str, "category": str}
    _defaults = {"geoInfoReference": '', "corporateCode": '', "direction": '', "category": ''}
    _enums = {}
    _refs = ["PositionPoints", "PowerSystemResources", "CoordinateSystems", "Measurements", "secondaryAddress", "Assets", "phone2", "electronicAddress", "phone1", "mainAddress", "status"]
    _many_refs = ["PositionPoints", "PowerSystemResources", "CoordinateSystems", "Measurements", "Assets"]

    def getPositionPoints(self):
        """Sequence of position points describing this location.
        """
        return self._PositionPoints

    def setPositionPoints(self, value):
        for x in self._PositionPoints:
            x._Location = None
        for y in value:
            y._Location = self
        self._PositionPoints = value

    PositionPoints = property(getPositionPoints, setPositionPoints)

    def addPositionPoints(self, *PositionPoints):
        for obj in PositionPoints:
            obj._Location = self
            self._PositionPoints.append(obj)

    def removePositionPoints(self, *PositionPoints):
        for obj in PositionPoints:
            obj._Location = None
            self._PositionPoints.remove(obj)

    def getPowerSystemResources(self):
        """All power system resources at this location.
        """
        return self._PowerSystemResources

    def setPowerSystemResources(self, value):
        for x in self._PowerSystemResources:
            x._Location = None
        for y in value:
            y._Location = self
        self._PowerSystemResources = value

    PowerSystemResources = property(getPowerSystemResources, setPowerSystemResources)

    def addPowerSystemResources(self, *PowerSystemResources):
        for obj in PowerSystemResources:
            obj._Location = self
            self._PowerSystemResources.append(obj)

    def removePowerSystemResources(self, *PowerSystemResources):
        for obj in PowerSystemResources:
            obj._Location = None
            self._PowerSystemResources.remove(obj)

    def getCoordinateSystems(self):
        """All coordinate systems used to describe position points of this location.
        """
        return self._CoordinateSystems

    def setCoordinateSystems(self, value):
        for x in self._CoordinateSystems:
            x._Location = None
        for y in value:
            y._Location = self
        self._CoordinateSystems = value

    CoordinateSystems = property(getCoordinateSystems, setCoordinateSystems)

    def addCoordinateSystems(self, *CoordinateSystems):
        for obj in CoordinateSystems:
            obj._Location = self
            self._CoordinateSystems.append(obj)

    def removeCoordinateSystems(self, *CoordinateSystems):
        for obj in CoordinateSystems:
            obj._Location = None
            self._CoordinateSystems.remove(obj)

    def getMeasurements(self):
        
        return self._Measurements

    def setMeasurements(self, value):
        for p in self._Measurements:
            filtered = [q for q in p.Locations if q != self]
            self._Measurements._Locations = filtered
        for r in value:
            if self not in r._Locations:
                r._Locations.append(self)
        self._Measurements = value

    Measurements = property(getMeasurements, setMeasurements)

    def addMeasurements(self, *Measurements):
        for obj in Measurements:
            if self not in obj._Locations:
                obj._Locations.append(self)
            self._Measurements.append(obj)

    def removeMeasurements(self, *Measurements):
        for obj in Measurements:
            if self in obj._Locations:
                obj._Locations.remove(self)
            self._Measurements.remove(obj)

    # Secondary address of the location. For example, PO Box address may have different ZIP code than that in the 'mainAddress'.
    secondaryAddress = None

    def getAssets(self):
        """All assets at this location.
        """
        return self._Assets

    def setAssets(self, value):
        for x in self._Assets:
            x._Location = None
        for y in value:
            y._Location = self
        self._Assets = value

    Assets = property(getAssets, setAssets)

    def addAssets(self, *Assets):
        for obj in Assets:
            obj._Location = self
            self._Assets.append(obj)

    def removeAssets(self, *Assets):
        for obj in Assets:
            obj._Location = None
            self._Assets.remove(obj)

    # Additional phone number.
    phone2 = None

    # Electronic address.
    electronicAddress = None

    # Phone number.
    phone1 = None

    # Main address of the location.
    mainAddress = None

    # Status of this location.
    status = None

