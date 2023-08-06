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

class BasePower(IdentifiedObject):
    """The BasePower class defines the base power used in the per unit calculations.
    """

    def __init__(self, basePower=0.0, *args, **kw_args):
        """Initialises a new 'BasePower' instance.

        @param basePower: Definition of base power. 
        """
        #: Definition of base power.
        self.basePower = basePower

        super(BasePower, self).__init__(*args, **kw_args)

    _attrs = ["basePower"]
    _attr_types = {"basePower": float}
    _defaults = {"basePower": 0.0}
    _enums = {}
    _refs = []
    _many_refs = []

