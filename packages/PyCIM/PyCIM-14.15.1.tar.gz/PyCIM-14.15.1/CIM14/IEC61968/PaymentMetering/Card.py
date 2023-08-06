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

class Card(Element):
    """Documentation of the tender when it is a type of card (credit, debit, etc).
    """

    def __init__(self, pan='', expiryDate='', cvNumber='', accountHolderName='', Tender=None, *args, **kw_args):
        """Initialises a new 'Card' instance.

        @param pan: The primary account number. 
        @param expiryDate: The date when this card expires. 
        @param cvNumber: The card verification number. 
        @param accountHolderName: Name of account holder. 
        @param Tender: Payment tender this card is being used for.
        """
        #: The primary account number.
        self.pan = pan

        #: The date when this card expires.
        self.expiryDate = expiryDate

        #: The card verification number.
        self.cvNumber = cvNumber

        #: Name of account holder.
        self.accountHolderName = accountHolderName

        self._Tender = None
        self.Tender = Tender

        super(Card, self).__init__(*args, **kw_args)

    _attrs = ["pan", "expiryDate", "cvNumber", "accountHolderName"]
    _attr_types = {"pan": str, "expiryDate": str, "cvNumber": str, "accountHolderName": str}
    _defaults = {"pan": '', "expiryDate": '', "cvNumber": '', "accountHolderName": ''}
    _enums = {}
    _refs = ["Tender"]
    _many_refs = []

    def getTender(self):
        """Payment tender this card is being used for.
        """
        return self._Tender

    def setTender(self, value):
        if self._Tender is not None:
            self._Tender._Card = None

        self._Tender = value
        if self._Tender is not None:
            self._Tender._Card = self

    Tender = property(getTender, setTender)

