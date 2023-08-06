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

from CIM14.CDPSM.Balanced.IEC61968.AssetModels.ConductorInfo import ConductorInfo

class OverheadConductorInfo(ConductorInfo):
    """Overhead conductor data.
    """

    def __init__(self, neutralInsulationThickness=0.0, phaseConductorCount=0, phaseConductorSpacing=0.0, *args, **kw_args):
        """Initialises a new 'OverheadConductorInfo' instance.

        @param neutralInsulationThickness: (if applicable) Insulation thickness of the neutral conductor. 
        @param phaseConductorCount: Number of conductor strands in the symmetrical bundle (1-12). 
        @param phaseConductorSpacing: Distance between conductor strands in a symmetrical bundle. 
        """
        #: (if applicable) Insulation thickness of the neutral conductor.
        self.neutralInsulationThickness = neutralInsulationThickness

        #: Number of conductor strands in the symmetrical bundle (1-12).
        self.phaseConductorCount = phaseConductorCount

        #: Distance between conductor strands in a symmetrical bundle.
        self.phaseConductorSpacing = phaseConductorSpacing

        super(OverheadConductorInfo, self).__init__(*args, **kw_args)

    _attrs = ["neutralInsulationThickness", "phaseConductorCount", "phaseConductorSpacing"]
    _attr_types = {"neutralInsulationThickness": float, "phaseConductorCount": int, "phaseConductorSpacing": float}
    _defaults = {"neutralInsulationThickness": 0.0, "phaseConductorCount": 0, "phaseConductorSpacing": 0.0}
    _enums = {}
    _refs = []
    _many_refs = []

