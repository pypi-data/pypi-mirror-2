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

"""This package contains the core information classes that support work management and network extension planning applications.
"""

nsPrefix = "cimWork"
nsURI = "http://iec.ch/TC57/2009/CIM-schema-cim14#Work"

from CIM14.IEC61968.Work.Work import Work

class WorkKind(str):
    """Kind of work.
    Values are: construction, maintenance, reconnect, meter, service, disconnect, inspection, other
    """
    pass
