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

from CIM14.Dynamics.TurbineGovernors.TurbineGovernor import TurbineGovernor

class GovHydro1(TurbineGovernor):
    """Hydro turbine-governor model.
    """

    def __init__(self, tf=0.0, velm=0.0, mwbase=0.0, gmin=0.0, gmax=0.0, rperm=0.0, tr=0.0, rtemp=0.0, qnl=0.0, tg=0.0, dturb=0.0, at=0.0, tw=0.0, HydroTurbine=None, synchronousMachine0=None, *args, **kw_args):
        """Initialises a new 'GovHydro1' instance.

        @param tf: Filter time constant (&gt;0) 
        @param velm: Maximum gate velocity (&gt;0) 
        @param mwbase: Base for power values  (&gt; 0.) 
        @param gmin: Minimum gate opening (&gt;=0) 
        @param gmax: Maximum gate opening (&gt;0) 
        @param rperm: Permanent droop (R) (&gt;0) 
        @param tr: Washout time constant (&gt;0) 
        @param rtemp: Temporary droop (r) (&gt;R) 
        @param qnl: No-load flow at nominal head (&gt;=0) 
        @param tg: Gate servo time constant (&gt;0) 
        @param dturb: Turbine damping factor (&gt;=0) 
        @param at: Turbine gain (&gt;0) 
        @param tw: Water inertia time constant (&gt;0) 
        @param HydroTurbine:
        @param synchronousMachine0:
        """
        #: Filter time constant (&gt;0)
        self.tf = tf

        #: Maximum gate velocity (&gt;0)
        self.velm = velm

        #: Base for power values  (&gt; 0.)
        self.mwbase = mwbase

        #: Minimum gate opening (&gt;=0)
        self.gmin = gmin

        #: Maximum gate opening (&gt;0)
        self.gmax = gmax

        #: Permanent droop (R) (&gt;0)
        self.rperm = rperm

        #: Washout time constant (&gt;0)
        self.tr = tr

        #: Temporary droop (r) (&gt;R)
        self.rtemp = rtemp

        #: No-load flow at nominal head (&gt;=0)
        self.qnl = qnl

        #: Gate servo time constant (&gt;0)
        self.tg = tg

        #: Turbine damping factor (&gt;=0)
        self.dturb = dturb

        #: Turbine gain (&gt;0)
        self.at = at

        #: Water inertia time constant (&gt;0)
        self.tw = tw

        self._HydroTurbine = None
        self.HydroTurbine = HydroTurbine

        self._synchronousMachine0 = []
        self.synchronousMachine0 = [] if synchronousMachine0 is None else synchronousMachine0

        super(GovHydro1, self).__init__(*args, **kw_args)

    _attrs = ["tf", "velm", "mwbase", "gmin", "gmax", "rperm", "tr", "rtemp", "qnl", "tg", "dturb", "at", "tw"]
    _attr_types = {"tf": float, "velm": float, "mwbase": float, "gmin": float, "gmax": float, "rperm": float, "tr": float, "rtemp": float, "qnl": float, "tg": float, "dturb": float, "at": float, "tw": float}
    _defaults = {"tf": 0.0, "velm": 0.0, "mwbase": 0.0, "gmin": 0.0, "gmax": 0.0, "rperm": 0.0, "tr": 0.0, "rtemp": 0.0, "qnl": 0.0, "tg": 0.0, "dturb": 0.0, "at": 0.0, "tw": 0.0}
    _enums = {}
    _refs = ["HydroTurbine", "synchronousMachine0"]
    _many_refs = ["synchronousMachine0"]

    def getHydroTurbine(self):
        
        return self._HydroTurbine

    def setHydroTurbine(self, value):
        if self._HydroTurbine is not None:
            self._HydroTurbine._HydroTurbineGovernor = None

        self._HydroTurbine = value
        if self._HydroTurbine is not None:
            self._HydroTurbine._HydroTurbineGovernor = self

    HydroTurbine = property(getHydroTurbine, setHydroTurbine)

    def getsynchronousMachine0(self):
        
        return self._synchronousMachine0

    def setsynchronousMachine0(self, value):
        for p in self._synchronousMachine0:
            filtered = [q for q in p.govHydro10 if q != self]
            self._synchronousMachine0._govHydro10 = filtered
        for r in value:
            if self not in r._govHydro10:
                r._govHydro10.append(self)
        self._synchronousMachine0 = value

    synchronousMachine0 = property(getsynchronousMachine0, setsynchronousMachine0)

    def addsynchronousMachine0(self, *synchronousMachine0):
        for obj in synchronousMachine0:
            if self not in obj._govHydro10:
                obj._govHydro10.append(self)
            self._synchronousMachine0.append(obj)

    def removesynchronousMachine0(self, *synchronousMachine0):
        for obj in synchronousMachine0:
            if self in obj._govHydro10:
                obj._govHydro10.remove(self)
            self._synchronousMachine0.remove(obj)

