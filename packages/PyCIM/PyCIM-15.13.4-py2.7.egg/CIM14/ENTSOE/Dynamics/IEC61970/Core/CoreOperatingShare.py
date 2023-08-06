# Copyright (C) 2010-2011 Richard Lincoln
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from CIM14.ENTSOE.Dynamics.Element import Element

class CoreOperatingShare(Element):

    def __init__(self, PowerSystemResource=None, *args, **kw_args):
        """Initialises a new 'CoreOperatingShare' instance.

        @param PowerSystemResource: 
        """
        self._PowerSystemResource = None
        self.PowerSystemResource = PowerSystemResource

        super(CoreOperatingShare, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["PowerSystemResource"]
    _many_refs = []

    def getPowerSystemResource(self):
        """
        """
        return self._PowerSystemResource

    def setPowerSystemResource(self, value):
        if self._PowerSystemResource is not None:
            filtered = [x for x in self.PowerSystemResource.OperatingShare if x != self]
            self._PowerSystemResource._OperatingShare = filtered

        self._PowerSystemResource = value
        if self._PowerSystemResource is not None:
            if self not in self._PowerSystemResource._OperatingShare:
                self._PowerSystemResource._OperatingShare.append(self)

    PowerSystemResource = property(getPowerSystemResource, setPowerSystemResource)

