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

class ExpressionInfo(object):
    """
    The ExpressionInfo objects are the actual "Core" of eos,
    they are what eventually applies an effect onto a fit.
    Which causes modules to actually do useful(tm) things.
    They are typically generated by the ExpressionBuild class
    but nothing prevents a user from making some of his own and running them onto a fit
    """
    def __init__(self):
        self.type = None
        """
        Type of the instance, describes which modification should be applied onto targets.
        """

        self.target = None
        """
        The target of this expression.
        May specify some destination location or filter, depending on info type.
        """

        self.operation = None
        """
        Which operation should be applied.
        Any other values will be ignored, causing the ExpressionInfo to do nothing
        """

        self.targetAttributeId = None
        """
        Which attribute will be affected by the operation on the target.
        This will be used as dictionary lookup key on all matched targets (if any)
        """

        self.sourceAttributeId = None
        """
        Which source attribute will be used as calculation base for the operation.
        This will be used as dictionary lookup key on the owner passed to the run method
        """

    def validate(self):
        # Usual assortment of checks, applicable to any info object
        if self.operation is None or self.targetAttributeId is None or \
        self.sourceAttributeId is None:
            return False
        # For direct assignments, we must ensure that we target item directly
        if self.type == const.infoAddItmMod:
            if self.target in const.locConvMap.values():
                return True
        # For location+group filters, check possible target location and presence of group specifier
        elif self.type == const.infoAddLocGrpMod:
            try:
                filterLoc, filterGrp = self.target
            except (TypeError, ValueError):
                return False
            validLocs = (const.locChar, const.locShip)
            if filterLoc in validLocs and filterGrp is not None:
                return True
        # For location, check possible target location
        elif self.type == const.infoAddLocMod:
            validLocs = (const.locChar, const.locShip)
            if self.target in validLocs:
                return True
        # For location+skill requirement filters, check possible target location and presence of
        # skill requirement specifier
        elif self.type == const.infoAddLocSrqMod:
            try:
                filterLoc, filterSrq = self.target
            except (TypeError, ValueError):
                return False
            validLocs = (const.locChar, const.locShip)
            if filterLoc in validLocs and filterSrq is not None:
                return True
        # For owner+skill requirement filters, check if target is character and presence
        # of skill requirement specifier
        elif self.type == const.infoAddOwnSrqMod:
            try:
                filterOwn, filterSrq = self.target
            except (TypeError, ValueError):
                return False
            if filterOwn is const.locChar and filterSrq is not None:
                return True
        # For direct gang modifications, target must be none (assumed it's ship)
        elif self.type == const.infoAddGangItmMod:
            if self.target is None:
                return True
        # For skill requirement filtered gang modification, target must be skill specifier
        elif self.type == const.infoAddGangSrqMod:
            if self.target is not None:
                return True
        # For group filtered gang modification, target must be group specifier
        elif self.type == const.infoAddGangGrpMod:
            if self.target is not None:
                return Tru
        # Mark all unknown for validator info types as invalid
        return False
