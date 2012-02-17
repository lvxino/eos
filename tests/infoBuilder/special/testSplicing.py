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
from eos.eve.effect import Effect
from eos.eve.expression import Expression
from eos.fit.attributeCalculator.info.infoBuilder import InfoBuilder
from eos.tests.infoBuilder.environment import Logger
from eos.tests.eosTestCase import EosTestCase


class TestSplicing(EosTestCase):
    """Test parsing of trees describing joins of multiple actual modifiers"""

    def testBuildSuccess(self):
        eTgtLoc = Expression(None, 24, value="Target")
        eTgtSrq = Expression(None, 29, expressionTypeId=3300)
        eTgtAttr1 = Expression(None, 22, expressionAttributeId=54)
        eTgtAttr2 = Expression(None, 22, expressionAttributeId=158)
        eTgtAttr3 = Expression(None, 22, expressionAttributeId=160)
        eOptr = Expression(None, 21, value="PostPercent")
        eSrcAttr1 = Expression(None, 22, expressionAttributeId=351)
        eSrcAttr2 = Expression(None, 22, expressionAttributeId=349)
        eSrcAttr3 = Expression(None, 22, expressionAttributeId=767)
        eTgtItms = Expression(None, 49, arg1=eTgtLoc, arg2=eTgtSrq)
        eTgtSpec1 = Expression(None, 12, arg1=eTgtItms, arg2=eTgtAttr1)
        eTgtSpec2 = Expression(None, 12, arg1=eTgtItms, arg2=eTgtAttr2)
        eTgtSpec3 = Expression(None, 12, arg1=eTgtItms, arg2=eTgtAttr3)
        eOptrTgt1 = Expression(None, 31, arg1=eOptr, arg2=eTgtSpec1)
        eOptrTgt2 = Expression(None, 31, arg1=eOptr, arg2=eTgtSpec2)
        eOptrTgt3 = Expression(None, 31, arg1=eOptr, arg2=eTgtSpec3)
        eAddMod1 = Expression(None, 9, arg1=eOptrTgt1, arg2=eSrcAttr1)
        eAddMod2 = Expression(None, 9, arg1=eOptrTgt2, arg2=eSrcAttr2)
        eAddMod3 = Expression(None, 9, arg1=eOptrTgt3, arg2=eSrcAttr3)
        eRmMod1 = Expression(None, 61, arg1=eOptrTgt1, arg2=eSrcAttr1)
        eRmMod2 = Expression(None, 61, arg1=eOptrTgt2, arg2=eSrcAttr2)
        eRmMod3 = Expression(None, 61, arg1=eOptrTgt3, arg2=eSrcAttr3)
        eAddSplice1 = Expression(None, 17, arg1=eAddMod1, arg2=eAddMod3)
        eAddSplice2 = Expression(None, 17, arg1=eAddMod2, arg2=eAddSplice1)
        eRmSplice1 = Expression(None, 17, arg1=eRmMod1, arg2=eRmMod3)
        eRmSplice2 = Expression(None, 17, arg1=eRmMod2, arg2=eRmSplice1)
        effect = Effect(None, 0, preExpression=eAddSplice2, postExpression=eRmSplice2)
        infos, status = InfoBuilder().build(effect, Logger())
        self.assertEqual(status, EffectBuildStatus.okFull)
        self.assertEqual(len(infos), 3)