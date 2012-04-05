#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2012 Anton Vorobyov
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


from eos.const import EffectBuildStatus
from eos.fit.attributeCalculator.modifier.modifierBuilder import ModifierBuilder
from eos.util.cachedProperty import cachedproperty
from .override.effect import customizeEffect


class Effect:
    """
    Represents a single effect. Effects are the building blocks which describe what its carrier
    does with other items.
    """

    def __init__(self, dataHandler=None, effectId=None, categoryId=None,
                 isOffensive=None, isAssistance=None, fittingUsageChanceAttributeId=None,
                 preExpressionId=None, postExpressionId=None):
        # Data handler which was used to build this effect
        self._dataHandler = dataHandler

        # The unique ID of an effect
        self.id = effectId

        # Effect category actually describes type of effect, which determines
        # when it is applied - always, when item is active, overloaded, etc.
        self.categoryId = categoryId

        # Whether the effect is offensive (e.g. guns)
        self.isOffensive = bool(isOffensive) if isOffensive is not None else None

        # Whether the effect is helpful (e.g. remote repairers)
        self.isAssistance = bool(isAssistance) if isAssistance is not None else None

        # Data necessary to get preExpression of the effect
        self._preExpressionId = preExpressionId

        # Data necessary to get postExpression of the effect
        self._postExpressionId = postExpressionId

        # Stores Modifiers which are assigned to given effect
        self._modifiers = None

        # Stores expression->modifiers parsing status
        self.modifierStatus = EffectBuildStatus.notParsed

        # Replace some data according to eos needs
        customizeEffect(self)

    @cachedproperty
    def preExpression(self):
        """
        PreExpression is the expression that gets run when
        something is activated.

        Possible exceptions:
        ExpressionFetchError -- raised when data handler fails
        to fetch any expression in tree
        """
        if self._preExpressionId is None:
            return None
        expression = self._dataHandler.getExpression(self._preExpressionId)
        return expression

    @cachedproperty
    def postExpression(self):
        """
        PostExpression gets run when the something becomes disabled.

        Possible exceptions:
        ExpressionFetchError -- raised when data handler fails
        to fetch any expression in tree
        """
        if self._postExpressionId is None:
            return None
        expression = self._dataHandler.getExpression(self._postExpressionId)
        return expression

    def getModifiers(self, logger):
        """
        Get modifiers of effect.

        Positional arguments:
        logger -- instance of logger to use for error reporting

        Return value:
        Set with Modifier objects generated by effect
        """
        if self._modifiers is None:
            self._modifiers, self.modifierStatus = ModifierBuilder.build(self, logger)
        return self._modifiers
