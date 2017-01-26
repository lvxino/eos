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


from unittest.mock import Mock

from eos.const.eos import State
from eos.const.eve import Attribute, Effect
from eos.fit.item.mixin.damage_dealer import DamageDealerMixin
from tests.holder_mixin.mixin_testcase import HolderMixinTestCase


class TestHolderMixinDamageDoomsdayNominalVolley(HolderMixinTestCase):

    def setUp(self):
        super().setUp()
        mixin = self.instantiate_mixin(DamageDealerMixin, type_id=None)
        mixin._eve_type = Mock()
        mixin._eve_type.default_effect.id = Effect.super_weapon_amarr
        mixin._eve_type.default_effect._state = State.active
        mixin.attributes = {}
        mixin.state = State.active
        mixin.cycle_time = 0.5
        mixin.reactivation_delay = None
        mixin.charge = None
        mixin.fully_charged_cycles_max = None
        mixin.reload_time = None
        self.mixin = mixin

    def test_generic(self):
        mixin = self.mixin
        mixin.attributes[Attribute.em_damage] = 5.2
        mixin.attributes[Attribute.thermal_damage] = 6.3
        mixin.attributes[Attribute.kinetic_damage] = 7.4
        mixin.attributes[Attribute.explosive_damage] = 8.5
        volley = mixin.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5.2)
        self.assertAlmostEqual(volley.thermal, 6.3)
        self.assertAlmostEqual(volley.kinetic, 7.4)
        self.assertAlmostEqual(volley.explosive, 8.5)
        self.assertAlmostEqual(volley.total, 27.4)

    def test_multiplier(self):
        mixin = self.mixin
        mixin.attributes[Attribute.em_damage] = 5.2
        mixin.attributes[Attribute.thermal_damage] = 6.3
        mixin.attributes[Attribute.kinetic_damage] = 7.4
        mixin.attributes[Attribute.explosive_damage] = 8.5
        mixin.attributes[Attribute.damage_multiplier] = 2
        volley = mixin.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5.2)
        self.assertAlmostEqual(volley.thermal, 6.3)
        self.assertAlmostEqual(volley.kinetic, 7.4)
        self.assertAlmostEqual(volley.explosive, 8.5)
        self.assertAlmostEqual(volley.total, 27.4)

    def test_insufficient_state(self):
        mixin = self.mixin
        mixin.attributes[Attribute.em_damage] = 5.2
        mixin.attributes[Attribute.thermal_damage] = 6.3
        mixin.attributes[Attribute.kinetic_damage] = 7.4
        mixin.attributes[Attribute.explosive_damage] = 8.5
        mixin.state = State.online
        volley = mixin.get_nominal_volley()
        self.assertIsNone(volley.em)
        self.assertIsNone(volley.thermal)
        self.assertIsNone(volley.kinetic)
        self.assertIsNone(volley.explosive)
        self.assertIsNone(volley.total)

    def test_charge_attrs(self):
        mixin = self.mixin
        mixin.charge = Mock()
        mixin.charge.attributes = {}
        mixin.charge.attributes[Attribute.em_damage] = 5.2
        mixin.charge.attributes[Attribute.thermal_damage] = 6.3
        mixin.charge.attributes[Attribute.kinetic_damage] = 7.4
        mixin.charge.attributes[Attribute.explosive_damage] = 8.5
        volley = mixin.get_nominal_volley()
        self.assertIsNone(volley.em)
        self.assertIsNone(volley.thermal)
        self.assertIsNone(volley.kinetic)
        self.assertIsNone(volley.explosive)
        self.assertIsNone(volley.total)

    def test_cache(self):
        mixin = self.mixin
        mixin.attributes[Attribute.em_damage] = 5.2
        mixin.attributes[Attribute.thermal_damage] = 6.3
        mixin.attributes[Attribute.kinetic_damage] = 7.4
        mixin.attributes[Attribute.explosive_damage] = 8.5
        volley = mixin.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5.2)
        self.assertAlmostEqual(volley.thermal, 6.3)
        self.assertAlmostEqual(volley.kinetic, 7.4)
        self.assertAlmostEqual(volley.explosive, 8.5)
        self.assertAlmostEqual(volley.total, 27.4)
        profile = Mock(em=0.2, thermal=0.2, kinetic=0.8, explosive=1)
        volley = mixin.get_nominal_volley(target_resistances=profile)
        self.assertAlmostEqual(volley.em, 4.16)
        self.assertAlmostEqual(volley.thermal, 5.04)
        self.assertAlmostEqual(volley.kinetic, 1.48)
        self.assertAlmostEqual(volley.explosive, 0)
        self.assertAlmostEqual(volley.total, 10.68)
        mixin.attributes[Attribute.em_damage] = 52
        mixin.attributes[Attribute.thermal_damage] = 63
        mixin.attributes[Attribute.kinetic_damage] = 74
        mixin.attributes[Attribute.explosive_damage] = 85
        volley = mixin.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5.2)
        self.assertAlmostEqual(volley.thermal, 6.3)
        self.assertAlmostEqual(volley.kinetic, 7.4)
        self.assertAlmostEqual(volley.explosive, 8.5)
        self.assertAlmostEqual(volley.total, 27.4)
        profile = Mock(em=0.2, thermal=0.2, kinetic=0.8, explosive=1)
        volley = mixin.get_nominal_volley(target_resistances=profile)
        self.assertAlmostEqual(volley.em, 4.16)
        self.assertAlmostEqual(volley.thermal, 5.04)
        self.assertAlmostEqual(volley.kinetic, 1.48)
        self.assertAlmostEqual(volley.explosive, 0)
        self.assertAlmostEqual(volley.total, 10.68)

    def test_volatility(self):
        mixin = self.mixin
        mixin.attributes[Attribute.em_damage] = 5.2
        mixin.attributes[Attribute.thermal_damage] = 6.3
        mixin.attributes[Attribute.kinetic_damage] = 7.4
        mixin.attributes[Attribute.explosive_damage] = 8.5
        volley = mixin.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5.2)
        self.assertAlmostEqual(volley.thermal, 6.3)
        self.assertAlmostEqual(volley.kinetic, 7.4)
        self.assertAlmostEqual(volley.explosive, 8.5)
        self.assertAlmostEqual(volley.total, 27.4)
        profile = Mock(em=0.2, thermal=0.2, kinetic=0.8, explosive=1)
        volley = mixin.get_nominal_volley(target_resistances=profile)
        self.assertAlmostEqual(volley.em, 4.16)
        self.assertAlmostEqual(volley.thermal, 5.04)
        self.assertAlmostEqual(volley.kinetic, 1.48)
        self.assertAlmostEqual(volley.explosive, 0)
        self.assertAlmostEqual(volley.total, 10.68)
        mixin._clear_volatile_attrs()
        mixin.attributes[Attribute.em_damage] = 52
        mixin.attributes[Attribute.thermal_damage] = 63
        mixin.attributes[Attribute.kinetic_damage] = 74
        mixin.attributes[Attribute.explosive_damage] = 85
        volley = mixin.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 52)
        self.assertAlmostEqual(volley.thermal, 63)
        self.assertAlmostEqual(volley.kinetic, 74)
        self.assertAlmostEqual(volley.explosive, 85)
        self.assertAlmostEqual(volley.total, 274)
        profile = Mock(em=0.2, thermal=0.2, kinetic=0.8, explosive=1)
        volley = mixin.get_nominal_volley(target_resistances=profile)
        self.assertAlmostEqual(volley.em, 41.6)
        self.assertAlmostEqual(volley.thermal, 50.4)
        self.assertAlmostEqual(volley.kinetic, 14.8)
        self.assertAlmostEqual(volley.explosive, 0)
        self.assertAlmostEqual(volley.total, 106.8)
