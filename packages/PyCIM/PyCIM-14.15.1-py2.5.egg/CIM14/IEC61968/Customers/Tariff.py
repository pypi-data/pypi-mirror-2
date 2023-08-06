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

from CIM14.IEC61968.Common.Document import Document

class Tariff(Document):
    """Document, approved by the responsible regulatory agency, listing the terms and conditions, including a schedule of prices, under which utility services will be provided. It has a unique number within the state or province. For Rate Schedules it is frequently allocated by the affiliated Public Utilities Commission.
    """

    def __init__(self, startDate='', endDate='', TariffProfiles=None, PricingStructures=None, *args, **kw_args):
        """Initialises a new 'Tariff' instance.

        @param startDate: Date tariff was activated. 
        @param endDate: (if tariff became inactive) Date tariff was terminated. 
        @param TariffProfiles: All tariff profiles using this tariff.
        @param PricingStructures: All pricing structures using this tariff.
        """
        #: Date tariff was activated.
        self.startDate = startDate

        #: (if tariff became inactive) Date tariff was terminated.
        self.endDate = endDate

        self._TariffProfiles = []
        self.TariffProfiles = [] if TariffProfiles is None else TariffProfiles

        self._PricingStructures = []
        self.PricingStructures = [] if PricingStructures is None else PricingStructures

        super(Tariff, self).__init__(*args, **kw_args)

    _attrs = ["startDate", "endDate"]
    _attr_types = {"startDate": str, "endDate": str}
    _defaults = {"startDate": '', "endDate": ''}
    _enums = {}
    _refs = ["TariffProfiles", "PricingStructures"]
    _many_refs = ["TariffProfiles", "PricingStructures"]

    def getTariffProfiles(self):
        """All tariff profiles using this tariff.
        """
        return self._TariffProfiles

    def setTariffProfiles(self, value):
        for p in self._TariffProfiles:
            filtered = [q for q in p.Tariffs if q != self]
            self._TariffProfiles._Tariffs = filtered
        for r in value:
            if self not in r._Tariffs:
                r._Tariffs.append(self)
        self._TariffProfiles = value

    TariffProfiles = property(getTariffProfiles, setTariffProfiles)

    def addTariffProfiles(self, *TariffProfiles):
        for obj in TariffProfiles:
            if self not in obj._Tariffs:
                obj._Tariffs.append(self)
            self._TariffProfiles.append(obj)

    def removeTariffProfiles(self, *TariffProfiles):
        for obj in TariffProfiles:
            if self in obj._Tariffs:
                obj._Tariffs.remove(self)
            self._TariffProfiles.remove(obj)

    def getPricingStructures(self):
        """All pricing structures using this tariff.
        """
        return self._PricingStructures

    def setPricingStructures(self, value):
        for p in self._PricingStructures:
            filtered = [q for q in p.Tariffs if q != self]
            self._PricingStructures._Tariffs = filtered
        for r in value:
            if self not in r._Tariffs:
                r._Tariffs.append(self)
        self._PricingStructures = value

    PricingStructures = property(getPricingStructures, setPricingStructures)

    def addPricingStructures(self, *PricingStructures):
        for obj in PricingStructures:
            if self not in obj._Tariffs:
                obj._Tariffs.append(self)
            self._PricingStructures.append(obj)

    def removePricingStructures(self, *PricingStructures):
        for obj in PricingStructures:
            if self in obj._Tariffs:
                obj._Tariffs.remove(self)
            self._PricingStructures.remove(obj)

