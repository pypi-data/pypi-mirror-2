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

class TownDetail(Element):
    """Town details, in the context of address.
    """

    def __init__(self, code='', country='', stateOrProvince='', name='', section='', *args, **kw_args):
        """Initialises a new 'TownDetail' instance.

        @param code: Town code. 
        @param country: Name of the country. 
        @param stateOrProvince: Name of the state or province. 
        @param name: Town name. 
        @param section: Town section. For example, it is common for there to be 36 sections per township. 
        """
        #: Town code.
        self.code = code

        #: Name of the country.
        self.country = country

        #: Name of the state or province.
        self.stateOrProvince = stateOrProvince

        #: Town name.
        self.name = name

        #: Town section. For example, it is common for there to be 36 sections per township.
        self.section = section

        super(TownDetail, self).__init__(*args, **kw_args)

    _attrs = ["code", "country", "stateOrProvince", "name", "section"]
    _attr_types = {"code": str, "country": str, "stateOrProvince": str, "name": str, "section": str}
    _defaults = {"code": '', "country": '', "stateOrProvince": '', "name": '', "section": ''}
    _enums = {}
    _refs = []
    _many_refs = []

