#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from collections import namedtuple

from eos.const.eos import Restriction
from eos.const.eve import Attribute
from eos.fit.restrictionTracker.exception import RegisterValidationError
from eos.fit.restrictionTracker.register import RestrictionRegister


ChargeVolumeErrorData = namedtuple('ChargeVolumeErrorData', ('maxVolume', 'holderVolume'))


class ChargeVolumeRegister(RestrictionRegister):
    """
    Implements restriction:
    Volume of single charge loaded into container should not
    excess its capacity.

    Details:
    Charge volume and container capacity are taken from
    attributes of original item.
    """

    def __init__(self):
        self.__containers = set()

    def registerHolder(self, holder):
        # Ignore container holders without charge attribute
        if not hasattr(holder, 'charge'):
            return
        self.__containers.add(holder)

    def unregisterHolder(self, holder):
        self.__containers.discard(holder)

    def validate(self):
        taintedHolders = {}
        for container in self.__containers:
            charge = container.charge
            if charge is None:
                continue
            # Get volume and capacity with 0 as fallback, and
            # compare them, raising error when charge can't fit
            chargeVolume = charge.item.attributes.get(Attribute.volume, 0)
            containerCapacity = container.item.attributes.get(Attribute.capacity, 0)
            if chargeVolume > containerCapacity:
                taintedHolders[charge] = ChargeVolumeErrorData(maxVolume=containerCapacity,
                                                               holderVolume=chargeVolume)
        if taintedHolders:
            raise RegisterValidationError(taintedHolders)

    @property
    def restrictionType(self):
        return Restriction.chargeVolume
