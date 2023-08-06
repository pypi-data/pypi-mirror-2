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

class TimePoint(IdentifiedObject):
    """A point in time within a sequence of points in time relative to a TimeSchedule.
    """

    def __init__(self, relativeTimeInterval=0.0, sequenceNumber=0, dateTime='', TimeSchedule=None, status=None, window=None, *args, **kw_args):
        """Initialises a new 'TimePoint' instance.

        @param relativeTimeInterval: (if interval-based) A point in time relative to scheduled start time in 'TimeSchedule.scheduleInterval.start'. 
        @param sequenceNumber: (if sequence-based) Relative sequence number for this time point. 
        @param dateTime: Absolute date and time for this time point. For calendar-based time point, it is typically manually entered, while for interval-based or sequence-based time point it is derived. 
        @param TimeSchedule: Time schedule owning this time point.
        @param status: Status of this time point.
        @param window: Interval defining the window of time that this time point is valid (for example, seasonal, only on weekends, not on weekends, only 8:00 to 5:00, etc.).
        """
        #: (if interval-based) A point in time relative to scheduled start time in 'TimeSchedule.scheduleInterval.start'.
        self.relativeTimeInterval = relativeTimeInterval

        #: (if sequence-based) Relative sequence number for this time point.
        self.sequenceNumber = sequenceNumber

        #: Absolute date and time for this time point. For calendar-based time point, it is typically manually entered, while for interval-based or sequence-based time point it is derived.
        self.dateTime = dateTime

        self._TimeSchedule = None
        self.TimeSchedule = TimeSchedule

        self.status = status

        self.window = window

        super(TimePoint, self).__init__(*args, **kw_args)

    _attrs = ["relativeTimeInterval", "sequenceNumber", "dateTime"]
    _attr_types = {"relativeTimeInterval": float, "sequenceNumber": int, "dateTime": str}
    _defaults = {"relativeTimeInterval": 0.0, "sequenceNumber": 0, "dateTime": ''}
    _enums = {}
    _refs = ["TimeSchedule", "status", "window"]
    _many_refs = []

    def getTimeSchedule(self):
        """Time schedule owning this time point.
        """
        return self._TimeSchedule

    def setTimeSchedule(self, value):
        if self._TimeSchedule is not None:
            filtered = [x for x in self.TimeSchedule.TimePoints if x != self]
            self._TimeSchedule._TimePoints = filtered

        self._TimeSchedule = value
        if self._TimeSchedule is not None:
            if self not in self._TimeSchedule._TimePoints:
                self._TimeSchedule._TimePoints.append(self)

    TimeSchedule = property(getTimeSchedule, setTimeSchedule)

    # Status of this time point.
    status = None

    # Interval defining the window of time that this time point is valid (for example, seasonal, only on weekends, not on weekends, only 8:00 to 5:00, etc.).
    window = None

