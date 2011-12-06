#===============================================================================
# Copyright (C) 2011 Diego Duclos
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

import collections

from eos import const
from abc import ABCMeta
from abc import abstractproperty

RegistrationInfo = collections.namedtuple("RegistrationInfo", ("sourceHolder", "info"))

class MutableAttributeHolder:
    """
    Base attribute holder class inherited by all classes that need to keep track of modified attributes.
    This class holds a MutableAttributeMap to keep track of changes.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def location(self):
        ...

    @abstractproperty
    def specific(self):
        ...

    def __init__(self, type):
        """
        Constructor. Accepts a Type
        """
        self.fit = None
        """
        Which fit this holder is bound to
        """
        self.type = type
        """
        Which type this holder wraps
        """

        self.attributes = MutableAttributeMap(self)
        """
        Special dictionary subclass that holds modified attributes and data related to their calculation
        """

    def _register(self):
        """Registers this holder, called when a holder is added to a fit"""
        self.attributes._registerAll()

    def _unregister(self):
        """Unregisters this holder, called when a holder is removed from a fit"""
        self.attributes._unregisterAll()

class MutableAttributeMap(collections.Mapping):
    """
    MutableAttributeMap class, this class is what actually keeps track of modified attribute values and who modified what so undo can work as expected.
    """

    def __init__(self, holder):
        self.__holder = holder
        self.__modifiedAttributes = {}

        # The attribute register keeps track of what effects apply to what attribute
        self.__attributeRegister = {}

    def __getitem__(self, key):
        val = self.__modifiedAttributes.get(key)
        if val is None:
            # Should actually run calcs here instead :D
            self.__modifiedAttributes[key] = val = self.__calculate(key)

        return val

    def __len__(self):
        return len(self.keys())

    def __contains__(self, key):
        return key in self.__modifiedAttributes or key in self.__holder.type.attributes

    def __iter__(self):
        for k in self.keys():
            yield k

    def keys(self):
        return set(self.__modifiedAttributes.keys()).intersection(self.__holder.type.attributes.keys())

    def _registerAll(self):
        """
        Populate the attributeRegister completely with what affects us
        and also add ourselves onto anything we affect.

        This is called for newly added holders to populate them entirely
        """
        # Populate our affectors
        holder = self.__holder
        fit = holder.fit

        for registrationInfo in fit._getAffectors(holder):
            self._registerOne(registrationInfo)


        for info in holder.type.getInfos():
            registrationInfo = (holder, info)
            for affectee in fit._getAffectees(registrationInfo):
                affectee.attributes._registerOne(registrationInfo)


    def _registerOne(self, registrationInfo):
        _, info = registrationInfo
        s = self.__attributeRegister.get(info.targetAttributeId)
        if s is None:
            s = self.__attributeRegister[info.targetAttributeId] = set()

        s.add(registrationInfo)

        try:
            del self.__modifiedAttributes[info.targetAttributeId]
        except:
            pass

    def _unregisterAll(self):
        fit = self.__holder.fit
        for info in self.__holder.type.getInfos():
            registrationInfo = (self, info)
            for affectee in fit._getAffectees(registrationInfo):
                affectee.attributes._unregisterOne(registrationInfo)

        del self.__attributeRegister[:]
        del self.__modifiedAttributes[:]

    def _unregisterOne(self, registrationInfo):
        _, info = registrationInfo
        self.__attributeRegister[info.targetAttributeId].remove(registrationInfo)
        del self.__modifiedAttributes[info.targetAttributeId]

    def __calculate(self, attrId):
        """
        Run calculations to find the actual value of attribute with ID equal to attrID.
        All other attribute values are assumed to be final.
        This is obviously not always the case,
        if any of the dependencies of this calculation change, this attribute will get invalidated and thus recalculated when its next needed
        """

        base = self.__holder.type.attributes.get(attrId)

        try:
            attributeType = self.__holder.type.attributeTypes[attrId]
            stackable = attributeType.stackable

            register = sorted(self.__attributeRegister[attrId], key=lambda registrationInfo: registrationInfo[1].operation)

            result = base

            penalizedUp = set()
            penalizedDown = set()

            for registrationInfo in register:
                sourceHolder, info = registrationInfo
                operation = info.operation
                value = sourceHolder.attributes[info.sourceAttributeId]

                if not stackable and sourceHolder.categoryId not in const.penaltyImmuneCats \
                   and operation in (const.optrPreMul, const.optrPostMul, const.optrPreDiv, const.optrPostDiv):
                    isMul = operation in (const.optrPreMul, const.optrPostMul)

                    s = penalizedUp if ((isMul and value > 1) or (not isMul and value < 1)) else penalizedDown
                    s.add(registrationInfo)

                elif operation in (const.optrPreAssignment, const.optrPostAssignment):
                    result = value
                elif operation in (const.optrPreMul, const.optrPostMul):
                    result *= value
                elif operation == const.optrPostPercent:
                    result *= 1 + value / 100
                elif operation in (const.optrPreDiv, const.optrPostDiv):
                    result /= value
                elif operation == const.optrModAdd:
                    result += value
                elif operation == const.optrModSub:
                    result -= value

            return result
        except:
            return base