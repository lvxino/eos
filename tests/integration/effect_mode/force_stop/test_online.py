# ==============================================================================
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
# ==============================================================================


from eos import *
from eos.const.eve import EffectCategoryId
from eos.const.eve import EffectId
from tests.integration.effect_mode.testcase import EffectModeTestCase


class TestForceStopOnline(EffectModeTestCase):

    def test_stopped_on_add(self):
        effect = self.mkeffect(
            category_id=EffectCategoryId.online,
            modifiers=[self.modifier])
        online_effect = self.mkeffect(
            effect_id=EffectId.online,
            category_id=EffectCategoryId.online)
        item = ModuleHigh(
            self.mktype(
                attrs={self.tgt_attr.id: 10, self.src_attr.id: 2},
                effects=[effect, online_effect]).id,
            state=State.online)
        item.set_effect_mode(effect.id, EffectMode.force_stop)
        # Action
        self.fit.modules.high.append(item)
        # Verification
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_stopped_on_state_switch(self):
        effect = self.mkeffect(
            category_id=EffectCategoryId.online,
            modifiers=[self.modifier])
        online_effect = self.mkeffect(
            effect_id=EffectId.online,
            category_id=EffectCategoryId.online)
        item = ModuleHigh(
            self.mktype(
                attrs={self.tgt_attr.id: 10, self.src_attr.id: 2},
                effects=[effect, online_effect]).id,
            state=State.offline)
        item.set_effect_mode(effect.id, EffectMode.force_stop)
        self.fit.modules.high.append(item)
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Action
        item.state = State.online
        # Verification
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_stopped_on_mode_switch(self):
        effect = self.mkeffect(
            category_id=EffectCategoryId.online,
            modifiers=[self.modifier])
        online_effect = self.mkeffect(
            effect_id=EffectId.online,
            category_id=EffectCategoryId.online)
        item = ModuleHigh(
            self.mktype(
                attrs={self.tgt_attr.id: 10, self.src_attr.id: 2},
                effects=[effect, online_effect]).id,
            state=State.online)
        item.set_effect_mode(effect.id, EffectMode.force_run)
        self.fit.modules.high.append(item)
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 12)
        # Action
        item.set_effect_mode(effect.id, EffectMode.force_stop)
        # Verification
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_stopped_no_online_effect(self):
        effect = self.mkeffect(
            category_id=EffectCategoryId.online,
            modifiers=[self.modifier])
        item = ModuleHigh(
            self.mktype(
                attrs={self.tgt_attr.id: 10, self.src_attr.id: 2},
                effects=[effect]).id,
            state=State.online)
        item.set_effect_mode(effect.id, EffectMode.force_stop)
        # Action
        self.fit.modules.high.append(item)
        # Verification
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_stopped_disabled_online_effect(self):
        effect = self.mkeffect(
            category_id=EffectCategoryId.online,
            modifiers=[self.modifier])
        online_effect = self.mkeffect(
            effect_id=EffectId.online,
            category_id=EffectCategoryId.online)
        item = ModuleHigh(
            self.mktype(
                attrs={self.tgt_attr.id: 10, self.src_attr.id: 2},
                effects=[effect, online_effect]).id,
            state=State.online)
        item.set_effect_mode(effect.id, EffectMode.force_stop)
        item.set_effect_mode(online_effect.id, EffectMode.force_stop)
        # Action
        self.fit.modules.high.append(item)
        # Verification
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_stopped_insufficient_state(self):
        effect = self.mkeffect(
            category_id=EffectCategoryId.online,
            modifiers=[self.modifier])
        online_effect = self.mkeffect(
            effect_id=EffectId.online,
            category_id=EffectCategoryId.online)
        item = ModuleHigh(
            self.mktype(
                attrs={self.tgt_attr.id: 10, self.src_attr.id: 2},
                effects=[effect, online_effect]).id,
            state=State.offline)
        item.set_effect_mode(effect.id, EffectMode.force_stop)
        # Action
        self.fit.modules.high.append(item)
        # Verification
        self.assertAlmostEqual(item.attrs[self.tgt_attr.id], 10)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)