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

class AccountingUnit(Element):
    """Unit for accounting; use either 'energyUnit' or 'currencyUnit' to specify the unit for 'value'.
    """

    def __init__(self, multiplier="k", monetaryUnit="CNY", energyUnit=0.0, value=0.0, *args, **kw_args):
        """Initialises a new 'AccountingUnit' instance.

        @param multiplier: Multiplier for the 'energyUnit' or 'monetaryUnit'. Values are: "k", "d", "n", "M", "none", "G", "micro", "T", "c", "m", "p"
        @param monetaryUnit: Unit of currency. Values are: "CNY", "EUR", "INR", "AUD", "CHF", "DKK", "other", "RUR", "SEK", "GBP", "JPY", "NOK", "CAD", "USD"
        @param energyUnit: Unit of service. 
        @param value: Value expressed in applicable units. 
        """
        #: Multiplier for the 'energyUnit' or 'monetaryUnit'. Values are: "k", "d", "n", "M", "none", "G", "micro", "T", "c", "m", "p"
        self.multiplier = multiplier

        #: Unit of currency. Values are: "CNY", "EUR", "INR", "AUD", "CHF", "DKK", "other", "RUR", "SEK", "GBP", "JPY", "NOK", "CAD", "USD"
        self.monetaryUnit = monetaryUnit

        #: Unit of service.
        self.energyUnit = energyUnit

        #: Value expressed in applicable units.
        self.value = value

        super(AccountingUnit, self).__init__(*args, **kw_args)

    _attrs = ["multiplier", "monetaryUnit", "energyUnit", "value"]
    _attr_types = {"multiplier": str, "monetaryUnit": str, "energyUnit": float, "value": float}
    _defaults = {"multiplier": "k", "monetaryUnit": "CNY", "energyUnit": 0.0, "value": 0.0}
    _enums = {"multiplier": "UnitMultiplier", "monetaryUnit": "Currency"}
    _refs = []
    _many_refs = []

