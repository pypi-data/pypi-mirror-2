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

from CIM14.IEC61970.Core.PowerSystemResource import PowerSystemResource

class CogenerationPlant(PowerSystemResource):
    """A set of thermal generating units for the production of electrical energy and process steam (usually from the output of the steam turbines). The steam sendout is typically used for industrial purposes or for municipal heating and cooling.
    """

    def __init__(self, cogenLPSteamRating=0.0, cogenHPSendoutRating=0.0, ratedP=0.0, cogenLPSendoutRating=0.0, cogenHPSteamRating=0.0, ThermalGeneratingUnits=None, SteamSendoutSchedule=None, *args, **kw_args):
        """Initialises a new 'CogenerationPlant' instance.

        @param cogenLPSteamRating: The low pressure steam rating 
        @param cogenHPSendoutRating: The high pressure steam sendout 
        @param ratedP: The rated output active power of the cogeneration plant 
        @param cogenLPSendoutRating: The low pressure steam sendout 
        @param cogenHPSteamRating: The high pressure steam rating 
        @param ThermalGeneratingUnits: A thermal generating unit may be a member of a cogeneration plant
        @param SteamSendoutSchedule: A cogeneration plant has a steam sendout schedule
        """
        #: The low pressure steam rating
        self.cogenLPSteamRating = cogenLPSteamRating

        #: The high pressure steam sendout
        self.cogenHPSendoutRating = cogenHPSendoutRating

        #: The rated output active power of the cogeneration plant
        self.ratedP = ratedP

        #: The low pressure steam sendout
        self.cogenLPSendoutRating = cogenLPSendoutRating

        #: The high pressure steam rating
        self.cogenHPSteamRating = cogenHPSteamRating

        self._ThermalGeneratingUnits = []
        self.ThermalGeneratingUnits = [] if ThermalGeneratingUnits is None else ThermalGeneratingUnits

        self._SteamSendoutSchedule = None
        self.SteamSendoutSchedule = SteamSendoutSchedule

        super(CogenerationPlant, self).__init__(*args, **kw_args)

    _attrs = ["cogenLPSteamRating", "cogenHPSendoutRating", "ratedP", "cogenLPSendoutRating", "cogenHPSteamRating"]
    _attr_types = {"cogenLPSteamRating": float, "cogenHPSendoutRating": float, "ratedP": float, "cogenLPSendoutRating": float, "cogenHPSteamRating": float}
    _defaults = {"cogenLPSteamRating": 0.0, "cogenHPSendoutRating": 0.0, "ratedP": 0.0, "cogenLPSendoutRating": 0.0, "cogenHPSteamRating": 0.0}
    _enums = {}
    _refs = ["ThermalGeneratingUnits", "SteamSendoutSchedule"]
    _many_refs = ["ThermalGeneratingUnits"]

    def getThermalGeneratingUnits(self):
        """A thermal generating unit may be a member of a cogeneration plant
        """
        return self._ThermalGeneratingUnits

    def setThermalGeneratingUnits(self, value):
        for x in self._ThermalGeneratingUnits:
            x._CogenerationPlant = None
        for y in value:
            y._CogenerationPlant = self
        self._ThermalGeneratingUnits = value

    ThermalGeneratingUnits = property(getThermalGeneratingUnits, setThermalGeneratingUnits)

    def addThermalGeneratingUnits(self, *ThermalGeneratingUnits):
        for obj in ThermalGeneratingUnits:
            obj._CogenerationPlant = self
            self._ThermalGeneratingUnits.append(obj)

    def removeThermalGeneratingUnits(self, *ThermalGeneratingUnits):
        for obj in ThermalGeneratingUnits:
            obj._CogenerationPlant = None
            self._ThermalGeneratingUnits.remove(obj)

    def getSteamSendoutSchedule(self):
        """A cogeneration plant has a steam sendout schedule
        """
        return self._SteamSendoutSchedule

    def setSteamSendoutSchedule(self, value):
        if self._SteamSendoutSchedule is not None:
            self._SteamSendoutSchedule._CogenerationPlant = None

        self._SteamSendoutSchedule = value
        if self._SteamSendoutSchedule is not None:
            self._SteamSendoutSchedule._CogenerationPlant = self

    SteamSendoutSchedule = property(getSteamSendoutSchedule, setSteamSendoutSchedule)

