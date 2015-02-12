#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2015 Anton Vorobyov
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


from eos.const.eos import State, Domain, Scope, FilterType, Operator
from eos.const.eve import EffectCategory
from eos.data.cache_object.modifier import Modifier
from eos.tests.attribute_calculator.attrcalc_testcase import AttrCalcTestCase
from eos.tests.attribute_calculator.environment import IndependentItem, CharacterItem, ShipItem


class TestCleanupChainChange(AttrCalcTestCase):
    """Check that changed attribute damages all attributes which are relying on it"""

    def test_attribute(self):
        attr1 = self.ch.attribute(attribute_id=1)
        attr2 = self.ch.attribute(attribute_id=2)
        attr3 = self.ch.attribute(attribute_id=3)
        modifier1 = Modifier()
        modifier1.state = State.offline
        modifier1.scope = Scope.local
        modifier1.source_attribute_id = attr1.id
        modifier1.operator = Operator.post_mul
        modifier1.target_attribute_id = attr2.id
        modifier1.domain = Domain.ship
        modifier1.filter_type = None
        modifier1.filter_value = None
        effect1 = self.ch.effect(effect_id=1, category_id=EffectCategory.passive)
        effect1.modifiers = (modifier1,)
        holder1 = CharacterItem(self.ch.type_(type_id=1, effects=(effect1,), attributes={attr1.id: 5}))
        modifier2 = Modifier()
        modifier2.state = State.offline
        modifier2.scope = Scope.local
        modifier2.source_attribute_id = attr2.id
        modifier2.operator = Operator.post_percent
        modifier2.target_attribute_id = attr3.id
        modifier2.domain = Domain.ship
        modifier2.filter_type = FilterType.all_
        modifier2.filter_value = None
        effect2 = self.ch.effect(effect_id=2, category_id=EffectCategory.passive)
        effect2.modifiers = (modifier2,)
        holder2 = IndependentItem(self.ch.type_(type_id=2, effects=(effect2,), attributes={attr2.id: 7.5}))
        holder3 = ShipItem(self.ch.type_(type_id=3, attributes={attr3.id: 0.5}))
        self.fit.items.add(holder1)
        self.fit.ship = holder2
        self.fit.items.add(holder3)
        self.assertAlmostEqual(holder3.attributes[attr3.id], 0.6875)
        holder1.attributes[attr1.id] = 4
        # Manually changed attribute must trigger damaging whole chain
        # of attributes, effectively allowing us to recalculate its new value
        self.assertAlmostEqual(holder3.attributes[attr3.id], 0.65)
        self.fit.items.remove(holder1)
        self.fit.ship = None
        self.fit.items.remove(holder3)
        self.assertEqual(len(self.log), 0)
        self.assert_link_buffers_empty(self.fit)
