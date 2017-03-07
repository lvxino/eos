# ===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2017 Anton Vorobyov
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
# ===============================================================================


from eos import *
from eos.const.eos import State, ModifierTargetFilter, ModifierDomain, ModifierOperator
from eos.const.eve import EffectCategory
from eos.data.cache_object.modifier import DogmaModifier, ModificationCalculationError
from eos.data.cache_object.modifier.python import BasePythonModifier
from eos.fit.pubsub.message import InstrAttrValueChanged
from tests.integration.calculator.calculator_testcase import CalculatorTestCase


class TestModifierPython(CalculatorTestCase):

    def setUp(self):
        super().setUp()
        self.attr1 = attr1 = self.ch.attribute()
        self.attr2 = attr2 = self.ch.attribute()
        self.attr3 = attr3 = self.ch.attribute()

        class TestPythonModifier(BasePythonModifier):

            def __init__(self):
                BasePythonModifier.__init__(
                    self, tgt_filter=ModifierTargetFilter.item, tgt_domain=ModifierDomain.self,
                    tgt_filter_extra_arg=None, tgt_attr=attr1.id
                )

            def get_modification(self, carrier_item, fit):
                try:
                    carrier_attrs = carrier_item.attributes
                    ship_attrs = fit.ship.attributes
                except AttributeError as e:
                    raise ModificationCalculationError from e
                try:
                    carrier_mul = carrier_attrs[attr2.id]
                    ship_mul = ship_attrs[attr3.id]
                except KeyError as e:
                    raise ModificationCalculationError from e
                return ModifierOperator.post_mul, carrier_mul * ship_mul

            @property
            def revise_message_types(self):
                return {InstrAttrValueChanged}

            def revise_modification(self, message, carrier_item, fit):
                if (
                    (message.item is carrier_item and message.attr == attr2.id) or
                    (message.item is fit.ship and message.attr == attr3.id)
                ):
                    return True
                return False

        self.python_effect = self.ch.effect(category=EffectCategory.online, modifiers=(TestPythonModifier(),))
        self.fit.ship = Ship(self.ch.type(attributes={attr3.id: 3}).id)

    def test_enabling(self):
        item = ModuleHigh(self.ch.type(
            effects=(self.python_effect,), attributes={self.attr1.id: 100, self.attr2.id: 2}
        ).id)
        self.fit.modules.high.append(item)
        self.assertAlmostEqual(item.attributes[self.attr1.id], 100)
        # Action
        item.state = State.online
        # Verification
        self.assertAlmostEqual(item.attributes[self.attr1.id], 600)
        # Misc
        self.fit.modules.high.remove(item)
        self.fit.ship = None
        self.assert_fit_buffers_empty(self.fit)

    def test_disabling(self):
        item = ModuleHigh(self.ch.type(
            effects=(self.python_effect,), attributes={self.attr1.id: 100, self.attr2.id: 2}
        ).id)
        self.fit.modules.high.append(item)
        item.state = State.online
        self.assertAlmostEqual(item.attributes[self.attr1.id], 600)
        # Action
        item.state = State.offline
        # Verification
        self.assertAlmostEqual(item.attributes[self.attr1.id], 100)
        # Misc
        self.fit.modules.high.remove(item)
        self.fit.ship = None
        self.assert_fit_buffers_empty(self.fit)

    def test_target_recalc_attr_change(self):
        # Here dogma modifier changes value of one of attributes
        # which are used as source by python modifier, and sees if
        # python modifier target value is updated
        attr4 = self.ch.attribute()
        dogma_modifier = DogmaModifier(
            tgt_filter=ModifierTargetFilter.item,
            tgt_domain=ModifierDomain.self,
            tgt_attr=self.attr2.id,
            operator=ModifierOperator.post_mul,
            src_attr=attr4.id
        )
        dogma_effect = self.ch.effect(category=EffectCategory.active, modifiers=(dogma_modifier,))
        item = ModuleHigh(self.ch.type(
            effects=(self.python_effect, dogma_effect), attributes={self.attr1.id: 100, self.attr2.id: 2, attr4.id: 5}
        ).id)
        self.fit.modules.high.append(item)
        item.state = State.online
        self.assertAlmostEqual(item.attributes[self.attr1.id], 600)
        # Action
        item.state = State.active
        # Verification
        self.assertAlmostEqual(item.attributes[self.attr1.id], 3000)
        # Misc
        self.fit.modules.high.remove(item)
        self.fit.ship = None
        self.assert_fit_buffers_empty(self.fit)

    def test_unsubscription(self):
        # Make sure that when python modifier unsubscribes
        # from message type needed by calculator, calculator
        # still receives that message type
        dogma_modifier1 = DogmaModifier(
            tgt_filter=ModifierTargetFilter.item,
            tgt_domain=ModifierDomain.self,
            tgt_attr=self.attr1.id,
            operator=ModifierOperator.post_mul,
            src_attr=self.attr2.id
        )
        dogma_effect1 = self.ch.effect(category=EffectCategory.passive, modifiers=(dogma_modifier1,))
        dogma_modifier2 = DogmaModifier(
            tgt_filter=ModifierTargetFilter.item,
            tgt_domain=ModifierDomain.self,
            tgt_attr=self.attr2.id,
            operator=ModifierOperator.post_mul,
            src_attr=self.attr3.id
        )
        dogma_effect2 = self.ch.effect(category=EffectCategory.online, modifiers=(dogma_modifier2,))
        python_item = ModuleHigh(self.ch.type(
            effects=(self.python_effect,), attributes={self.attr1.id: 100, self.attr2.id: 2}
        ).id)
        dogma_item = ModuleHigh(self.ch.type(
            effects=(dogma_effect1, dogma_effect2),
            attributes={self.attr1.id: 100, self.attr2.id: 2, self.attr3.id: 3}
        ).id)
        self.fit.modules.high.append(python_item)
        self.assertAlmostEqual(python_item.attributes[self.attr1.id], 100)
        python_item.state = State.online
        self.assertAlmostEqual(python_item.attributes[self.attr1.id], 600)
        self.fit.modules.high.remove(python_item)  # Here modifier is unsubscribed from attr change events
        self.fit.modules.high.append(dogma_item)
        self.assertAlmostEqual(dogma_item.attributes[self.attr1.id], 200)
        # Action
        dogma_item.state = State.online
        # Verification
        # If value is updated, then calculator service received attribute
        # updated message
        self.assertAlmostEqual(dogma_item.attributes[self.attr1.id], 600)
        # Misc
        self.fit.modules.high.remove(dogma_item)
        self.fit.ship = None
        self.assert_fit_buffers_empty(self.fit)
