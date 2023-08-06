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

from CIM14.Element import Element

class StreetAddress(Element):
    """General purpose street address information.
    """

    def __init__(self, status=None, townDetail=None, streetDetail=None, *args, **kw_args):
        """Initialises a new 'StreetAddress' instance.

        @param status: Status of this address.
        @param townDetail: Town detail.
        @param streetDetail: Street detail.
        """
        self.status = status

        self.townDetail = townDetail

        self.streetDetail = streetDetail

        super(StreetAddress, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["status", "townDetail", "streetDetail"]
    _many_refs = []

    # Status of this address.
    status = None

    # Town detail.
    townDetail = None

    # Street detail.
    streetDetail = None

