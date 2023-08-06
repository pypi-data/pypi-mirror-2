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

from CIM14.IEC61968.Common.Location import Location

class ServiceLocation(Location):
    """A customer ServiceLocation has one or more ServiceDeliveryPoint(s), which in turn relate to Meters. The location may be a point or a polygon, depending on the specific circumstances. For distribution, the ServiceLocation is typically the location of the utility customer's premise. Because a customer's premise may have one or more meters, the ServiceDeliveryPoint is used to define the actual conducting equipment that the EndDeviceAsset attaches to at the utility customer's ServiceLocation. For transmission, it is the point(s) of interconnection on the transmission provider's transmission system where capacity and/or energy transmitted by the transmission provider is made available to the receiving party.
    """

    def __init__(self, siteAccessProblem='', accessMethod='', needsInspection=False, EndDeviceAssets=None, CustomerAgreements=None, ServiceDeliveryPoints=None, *args, **kw_args):
        """Initialises a new 'ServiceLocation' instance.

        @param siteAccessProblem: Problems previously encountered when visiting or performing work on this site. Examples include: bad dog, violent customer, verbally abusive occupant, obstructions, safety hazards, etc. 
        @param accessMethod: Method for the service person to access the appropriate service locations. For example, a description of where to obtain a key if the facility is unmanned and secured. 
        @param needsInspection: True if inspection is needed of facilities at this service location. This could be requested by a customer, due to suspected tampering, environmental concerns (e.g., a fire in the vicinity), or to correct incompatible data. 
        @param EndDeviceAssets: All end device assets that measure the service delivered to this service location.
        @param CustomerAgreements: All customer agreements regulating this service location.
        @param ServiceDeliveryPoints: All service delivery points delivering service (of the same type) to this service location.
        """
        #: Problems previously encountered when visiting or performing work on this site. Examples include: bad dog, violent customer, verbally abusive occupant, obstructions, safety hazards, etc.
        self.siteAccessProblem = siteAccessProblem

        #: Method for the service person to access the appropriate service locations. For example, a description of where to obtain a key if the facility is unmanned and secured.
        self.accessMethod = accessMethod

        #: True if inspection is needed of facilities at this service location. This could be requested by a customer, due to suspected tampering, environmental concerns (e.g., a fire in the vicinity), or to correct incompatible data.
        self.needsInspection = needsInspection

        self._EndDeviceAssets = []
        self.EndDeviceAssets = [] if EndDeviceAssets is None else EndDeviceAssets

        self._CustomerAgreements = []
        self.CustomerAgreements = [] if CustomerAgreements is None else CustomerAgreements

        self._ServiceDeliveryPoints = []
        self.ServiceDeliveryPoints = [] if ServiceDeliveryPoints is None else ServiceDeliveryPoints

        super(ServiceLocation, self).__init__(*args, **kw_args)

    _attrs = ["siteAccessProblem", "accessMethod", "needsInspection"]
    _attr_types = {"siteAccessProblem": str, "accessMethod": str, "needsInspection": bool}
    _defaults = {"siteAccessProblem": '', "accessMethod": '', "needsInspection": False}
    _enums = {}
    _refs = ["EndDeviceAssets", "CustomerAgreements", "ServiceDeliveryPoints"]
    _many_refs = ["EndDeviceAssets", "CustomerAgreements", "ServiceDeliveryPoints"]

    def getEndDeviceAssets(self):
        """All end device assets that measure the service delivered to this service location.
        """
        return self._EndDeviceAssets

    def setEndDeviceAssets(self, value):
        for x in self._EndDeviceAssets:
            x.ServiceLocation = None
        for y in value:
            y._ServiceLocation = self
        self._EndDeviceAssets = value

    EndDeviceAssets = property(getEndDeviceAssets, setEndDeviceAssets)

    def addEndDeviceAssets(self, *EndDeviceAssets):
        for obj in EndDeviceAssets:
            obj.ServiceLocation = self

    def removeEndDeviceAssets(self, *EndDeviceAssets):
        for obj in EndDeviceAssets:
            obj.ServiceLocation = None

    def getCustomerAgreements(self):
        """All customer agreements regulating this service location.
        """
        return self._CustomerAgreements

    def setCustomerAgreements(self, value):
        for p in self._CustomerAgreements:
            filtered = [q for q in p.ServiceLocations if q != self]
            self._CustomerAgreements._ServiceLocations = filtered
        for r in value:
            if self not in r._ServiceLocations:
                r._ServiceLocations.append(self)
        self._CustomerAgreements = value

    CustomerAgreements = property(getCustomerAgreements, setCustomerAgreements)

    def addCustomerAgreements(self, *CustomerAgreements):
        for obj in CustomerAgreements:
            if self not in obj._ServiceLocations:
                obj._ServiceLocations.append(self)
            self._CustomerAgreements.append(obj)

    def removeCustomerAgreements(self, *CustomerAgreements):
        for obj in CustomerAgreements:
            if self in obj._ServiceLocations:
                obj._ServiceLocations.remove(self)
            self._CustomerAgreements.remove(obj)

    def getServiceDeliveryPoints(self):
        """All service delivery points delivering service (of the same type) to this service location.
        """
        return self._ServiceDeliveryPoints

    def setServiceDeliveryPoints(self, value):
        for x in self._ServiceDeliveryPoints:
            x.ServiceLocation = None
        for y in value:
            y._ServiceLocation = self
        self._ServiceDeliveryPoints = value

    ServiceDeliveryPoints = property(getServiceDeliveryPoints, setServiceDeliveryPoints)

    def addServiceDeliveryPoints(self, *ServiceDeliveryPoints):
        for obj in ServiceDeliveryPoints:
            obj.ServiceLocation = self

    def removeServiceDeliveryPoints(self, *ServiceDeliveryPoints):
        for obj in ServiceDeliveryPoints:
            obj.ServiceLocation = None

