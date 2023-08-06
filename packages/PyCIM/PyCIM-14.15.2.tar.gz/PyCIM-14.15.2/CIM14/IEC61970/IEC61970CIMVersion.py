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

class IEC61970CIMVersion(Element):
    """This is the IEC 61970 CIM version number assigned to this UML model file.
    """

    def __init__(self, version='', date='', *args, **kw_args):
        """Initialises a new 'IEC61970CIMVersion' instance.

        @param version: Form is IEC61970CIMXXvYY where XX is the major CIM package version and the YY is the minor version. For ecample IEC61970CIM13v18. 
        @param date: Form is YYYY-MM-DD for example for January 5, 2009 it is 2009-01-05. 
        """
        #: Form is IEC61970CIMXXvYY where XX is the major CIM package version and the YY is the minor version. For ecample IEC61970CIM13v18.
        self.version = version

        #: Form is YYYY-MM-DD for example for January 5, 2009 it is 2009-01-05.
        self.date = date

        super(IEC61970CIMVersion, self).__init__(*args, **kw_args)

    _attrs = ["version", "date"]
    _attr_types = {"version": str, "date": str}
    _defaults = {"version": '', "date": ''}
    _enums = {}
    _refs = []
    _many_refs = []

