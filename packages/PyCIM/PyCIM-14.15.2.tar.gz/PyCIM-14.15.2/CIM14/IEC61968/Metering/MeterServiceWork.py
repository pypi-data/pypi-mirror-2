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

from CIM14.IEC61968.Work.Work import Work

class MeterServiceWork(Work):
    """Work involving meters.
    """

    def __init__(self, OldMeterAsset=None, MeterAsset=None, *args, **kw_args):
        """Initialises a new 'MeterServiceWork' instance.

        @param OldMeterAsset: Old meter asset replaced by this work.
        @param MeterAsset: Meter asset on which this non-replacement work is performed.
        """
        self._OldMeterAsset = None
        self.OldMeterAsset = OldMeterAsset

        self._MeterAsset = None
        self.MeterAsset = MeterAsset

        super(MeterServiceWork, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["OldMeterAsset", "MeterAsset"]
    _many_refs = []

    def getOldMeterAsset(self):
        """Old meter asset replaced by this work.
        """
        return self._OldMeterAsset

    def setOldMeterAsset(self, value):
        if self._OldMeterAsset is not None:
            filtered = [x for x in self.OldMeterAsset.MeterReplacementWorks if x != self]
            self._OldMeterAsset._MeterReplacementWorks = filtered

        self._OldMeterAsset = value
        if self._OldMeterAsset is not None:
            if self not in self._OldMeterAsset._MeterReplacementWorks:
                self._OldMeterAsset._MeterReplacementWorks.append(self)

    OldMeterAsset = property(getOldMeterAsset, setOldMeterAsset)

    def getMeterAsset(self):
        """Meter asset on which this non-replacement work is performed.
        """
        return self._MeterAsset

    def setMeterAsset(self, value):
        if self._MeterAsset is not None:
            filtered = [x for x in self.MeterAsset.MeterServiceWorks if x != self]
            self._MeterAsset._MeterServiceWorks = filtered

        self._MeterAsset = value
        if self._MeterAsset is not None:
            if self not in self._MeterAsset._MeterServiceWorks:
                self._MeterAsset._MeterServiceWorks.append(self)

    MeterAsset = property(getMeterAsset, setMeterAsset)

