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

class TargetLevelSchedule(Curve):
    """Reservoir water level targets from advanced studies or 'rule curves'. Typically in one hour increments for up to 10 days
    """

    def __init__(self, highLevelLimit=0.0, lowLevelLimit=0.0, Reservoir=None, *args, **kw_args):
        """Initialises a new 'TargetLevelSchedule' instance.

        @param highLevelLimit: High target level limit, above which the reservoir operation will be penalized 
        @param lowLevelLimit: Low target level limit, below which the reservoir operation will be penalized 
        @param Reservoir: A reservoir may have a water level target schedule.
        """
        #: High target level limit, above which the reservoir operation will be penalized
        self.highLevelLimit = highLevelLimit

        #: Low target level limit, below which the reservoir operation will be penalized
        self.lowLevelLimit = lowLevelLimit

        self._Reservoir = None
        self.Reservoir = Reservoir

        super(TargetLevelSchedule, self).__init__(*args, **kw_args)

    _attrs = ["highLevelLimit", "lowLevelLimit"]
    _attr_types = {"highLevelLimit": float, "lowLevelLimit": float}
    _defaults = {"highLevelLimit": 0.0, "lowLevelLimit": 0.0}
    _enums = {}
    _refs = ["Reservoir"]
    _many_refs = []

    def getReservoir(self):
        """A reservoir may have a water level target schedule.
        """
        return self._Reservoir

    def setReservoir(self, value):
        if self._Reservoir is not None:
            self._Reservoir._TargetLevelSchedule = None

        self._Reservoir = value
        if self._Reservoir is not None:
            self._Reservoir.TargetLevelSchedule = None
            self._Reservoir._TargetLevelSchedule = self

    Reservoir = property(getReservoir, setReservoir)

