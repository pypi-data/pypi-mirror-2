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

from CIM14.IEC61970.Equivalents.EquivalentEquipment import EquivalentEquipment

class EquivalentBranch(EquivalentEquipment):
    """The class represents equivalent branches.
    """

    def __init__(self, x=0.0, r=0.0, *args, **kw_args):
        """Initialises a new 'EquivalentBranch' instance.

        @param x: Positive sequence series reactance of the reduced branch. 
        @param r: Positive sequence series resistance of the reduced branch. 
        """
        #: Positive sequence series reactance of the reduced branch.
        self.x = x

        #: Positive sequence series resistance of the reduced branch.
        self.r = r

        super(EquivalentBranch, self).__init__(*args, **kw_args)

    _attrs = ["x", "r"]
    _attr_types = {"x": float, "r": float}
    _defaults = {"x": 0.0, "r": 0.0}
    _enums = {}
    _refs = []
    _many_refs = []

