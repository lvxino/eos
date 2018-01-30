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


"""
This file holds IDs of multiple eve's entities.
"""


from enum import IntEnum
from enum import unique


@unique
class AttrId(IntEnum):
    # Resources
    cpu = 50
    cpu_output = 48
    drone_bandwidth = 1271
    drone_bandwidth_used = 1272
    power = 30
    power_output = 11
    upgrade_capacity = 1132
    upgrade_cost = 1153
    # Slots
    boosterness = 1087
    drone_capacity = 283
    hi_slots = 14
    implantness = 331
    launcher_slots_left = 101
    low_slots = 12
    max_active_drones = 352
    max_subsystems = 1367
    med_slots = 13
    rig_slots = 1137
    subsystem_slot = 1366
    turret_slots_left = 102
    # Damage
    em_dmg = 114
    explosive_dmg = 116
    kinetic_dmg = 117
    thermal_dmg = 118
    # Resistances
    armor_em_dmg_resonance = 267
    armor_explosive_dmg_resonance = 268
    armor_kinetic_dmg_resonance = 269
    armor_thermal_dmg_resonance = 270
    em_dmg_resonance = 113
    explosive_dmg_resonance = 111
    kinetic_dmg_resonance = 109
    resist_shift_amount = 1849
    thermal_dmg_resonance = 110
    shield_em_dmg_resonance = 271
    shield_explosive_dmg_resonance = 272
    shield_kinetic_dmg_resonance = 273
    shield_thermal_dmg_resonance = 274
    # Tanking
    armor_hp = 265
    hp = 9
    shield_capacity = 263
    # Repairing
    armor_dmg_amount = 84
    charged_armor_dmg_multiplier = 1886
    # Charge-related
    ammo_loaded = 127
    charge_group_1 = 604
    charge_group_2 = 605
    charge_group_3 = 606
    charge_group_4 = 609
    charge_group_5 = 610
    charge_rate = 56
    charge_size = 128
    crystal_volatility_chance = 783
    crystal_volatility_dmg = 784
    crystals_get_damaged = 786
    reload_time = 1795
    # Skills
    required_skill_1 = 182
    required_skill_1_level = 277
    required_skill_2 = 183
    required_skill_2_level = 278
    required_skill_3 = 184
    required_skill_3_level = 279
    required_skill_4 = 1285
    required_skill_4_level = 1286
    required_skill_5 = 1289
    required_skill_5_level = 1287
    required_skill_6 = 1290
    required_skill_6_level = 1288
    skill_level = 280
    # Fitting restriction
    allowed_drone_group_1 = 1782
    allowed_drone_group_2 = 1783
    can_fit_ship_group_1 = 1298
    can_fit_ship_group_2 = 1299
    can_fit_ship_group_3 = 1300
    can_fit_ship_group_4 = 1301
    can_fit_ship_group_5 = 1872
    can_fit_ship_group_6 = 1879
    can_fit_ship_group_7 = 1880
    can_fit_ship_group_8 = 1881
    can_fit_ship_group_9 = 2065
    can_fit_ship_group_10 = 2396
    can_fit_ship_group_11 = 2476
    can_fit_ship_group_12 = 2477
    can_fit_ship_group_13 = 2478
    can_fit_ship_group_14 = 2479
    can_fit_ship_group_15 = 2480
    can_fit_ship_group_16 = 2481
    can_fit_ship_group_17 = 2482
    can_fit_ship_group_18 = 2483
    can_fit_ship_group_19 = 2484
    can_fit_ship_group_20 = 2485
    can_fit_ship_type_1 = 1302
    can_fit_ship_type_2 = 1303
    can_fit_ship_type_3 = 1304
    can_fit_ship_type_4 = 1305
    can_fit_ship_type_5 = 1944
    can_fit_ship_type_6 = 2103
    can_fit_ship_type_7 = 2463
    can_fit_ship_type_8 = 2486
    can_fit_ship_type_9 = 2487
    can_fit_ship_type_10 = 2488
    fits_to_shiptype = 1380
    max_group_active = 763
    max_group_fitted = 1544
    max_group_online = 978
    rig_size = 1547
    # Fighters
    fighter_tubes = 2216
    fighter_support_slots = 2218
    fighter_light_slots = 2217
    fighter_heavy_slots = 2219
    fighter_squadron_is_heavy = 2214
    fighter_squadron_is_light = 2212
    fighter_squadron_is_support = 2213
    fighter_squadron_max_size = 2215
    fighter_ability_attack_missile_dmg_em = 2227
    fighter_ability_attack_missile_dmg_thermal = 2228
    fighter_ability_attack_missile_dmg_kinetic = 2229
    fighter_ability_attack_missile_dmg_explosive = 2230
    fighter_ability_attack_missile_dmg_multiplier = 2226
    # Misc
    agility = 70
    capacity = 38
    dmg_multiplier = 64
    is_capital_size = 1785
    mass = 4
    mass_addition = 796
    max_velocity = 37
    missile_dmg_multiplier = 212
    module_reactivation_delay = 669
    radius = 162
    signature_radius = 552
    signature_radius_bonus = 554
    speed_boost_factor = 567
    speed_factor = 20
    volume = 161


@unique
class TypeId(IntEnum):
    character_static = 1381
    missile_launcher_operation = 3319  # Skill
    nanite_repair_paste = 28668
    sentry_drone_interfacing = 23594  # Skill


@unique
class TypeGroupId(IntEnum):
    character = 1
    effect_beacon = 920
    energy_weapon = 53
    hydrid_weapon = 74
    mining_laser = 54
    projectile_weapon = 55
    ship_modifier = 1306


@unique
class TypeCategoryId(IntEnum):
    charge = 8
    drone = 18
    fighter = 87
    implant = 20
    module = 7
    ship = 6
    skill = 16
    subsystem = 32


@unique
class EffectId(IntEnum):
    adaptive_armor_hardener = 4928
    bomb_launching = 2971
    emp_wave = 38
    fighter_ability_afterburner = 6440
    fighter_ability_attack = 6430
    fighter_ability_attack_m = 6465
    fighter_ability_ecm = 6437
    fighter_ability_energy_neutralizer = 6434
    fighter_ability_evasive_maneuvers = 6439
    fighter_ability_kamikaze = 6554
    fighter_ability_launch_bomb = 6485
    fighter_ability_microjumpdrive = 6442
    fighter_ability_microwarpdrive = 6441
    fighter_ability_missiles = 6431
    fighter_ability_stasis_webifier = 6435
    fighter_ability_tackle = 6464
    fighter_ability_warp_disruption = 6436
    fighter_damage_multiply = 6420
    fighter_decrease_target_speed = 6418
    fighter_microjumpdrive = 6421
    fighter_target_paint = 6419
    fof_missile_launching = 104
    fueled_armor_repair = 5275
    hi_power = 12
    launcher_fitted = 40
    lo_power = 11
    med_power = 13
    mining_laser = 67
    missile_launching = 9
    module_bonus_afterburner = 6731
    module_bonus_ancillary_remote_armor_repairer = 6651
    module_bonus_microwarpdrive = 6730
    online = 16
    projectile_fired = 34
    rig_slot = 2663
    subsystem = 3772
    super_weapon_amarr = 4489
    super_weapon_caldari = 4490
    super_weapon_gallente = 4491
    super_weapon_minmatar = 4492
    target_attack = 10
    turret_fitted = 42
    use_missiles = 101


@unique
class EffectCategoryId(IntEnum):
    passive = 0
    active = 1
    target = 2
    area = 3
    online = 4
    overload = 5
    dungeon = 6
    system = 7


@unique
class FighterAbilityId(IntEnum):
    attack_turret = 1
    webs = 2
    tgt_paint = 3
    microwarpdrive = 4
    microjumpdrive = 5
    dmg_boost = 6
    launch_bomb = 7
    afterburner = 9
    warp_disrupt = 10
    energy_neut = 11
    ecm = 12
    evasion = 13
    missile = 14
    tackle = 16
    attack_missile = 17
    torpedo_salvo_em = 18
    torpedo_salvo_therm = 19
    torpedo_salvo_kin = 20
    torpedo_salvo_exp = 21
    pulse_cannon = 22
    beam_cannon = 23
    blaster_cannon = 24
    railgun = 25
    autocannon = 26
    artillery = 27
    micromissile_swarm_em = 29
    micromissile_swarm_therm = 30
    micromissile_swarm_kin = 31
    micromissile_swarm_exp = 32
    heavy_rocket_salvo_em = 33
    heavy_rocket_salvo_therm = 34
    heavy_rocket_salvo_kin = 35
    heavy_rocket_salvo_exp = 36
    kamikaze = 38
    blaster_cannon_caldari = 44
    railgun_caldari = 45


@unique
class OperandId(IntEnum):
    """Expression operand IDs."""
    add_dom_grp_mod = 7
    add_dom_mod = 8
    add_dom_srq_mod = 9
    add_itm_mod = 6
    add_own_srq_mod = 11
    def_attr = 22
    def_grp = 26
    def_int = 27
    def_dom = 24
    def_optr = 21
    def_type = 29
    dom_grp = 48  # Joins domain and group definitions
    dom_srq = 49  # Joins domain and skill requirement definitions
    get_type = 36
    itm_attr = 12  # Defines target - joins target items and attribute
    optr_tgt = 31  # Joins operator and target definitions
    rm_dom_grp_mod = 59
    rm_dom_mod = 60
    rm_dom_srq_mod = 61
    rm_itm_mod = 58
    rm_own_srq_mod = 62
    splice = 17  # Joins two modifiers


fighter_ability_map = {
    FighterAbilityId.attack_turret:
        EffectId.fighter_ability_attack,
    FighterAbilityId.webs:
        EffectId.fighter_ability_stasis_webifier,
    FighterAbilityId.tgt_paint:
        EffectId.fighter_target_paint,
    FighterAbilityId.warp_disrupt:
        EffectId.fighter_ability_warp_disruption,
    FighterAbilityId.energy_neut:
        EffectId.fighter_ability_energy_neutralizer,
    FighterAbilityId.ecm:
        EffectId.fighter_ability_ecm,
    FighterAbilityId.missile:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.tackle:
        EffectId.fighter_ability_tackle,
    FighterAbilityId.attack_missile:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.torpedo_salvo_em:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.torpedo_salvo_therm:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.torpedo_salvo_kin:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.torpedo_salvo_exp:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.pulse_cannon:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.beam_cannon:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.blaster_cannon:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.railgun:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.autocannon:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.artillery:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.micromissile_swarm_em:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.micromissile_swarm_therm:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.micromissile_swarm_kin:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.micromissile_swarm_exp:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.heavy_rocket_salvo_em:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.heavy_rocket_salvo_therm:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.heavy_rocket_salvo_kin:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.heavy_rocket_salvo_exp:
        EffectId.fighter_ability_missiles,
    FighterAbilityId.afterburner:
        EffectId.fighter_ability_afterburner,
    FighterAbilityId.microwarpdrive:
        EffectId.fighter_ability_microwarpdrive,
    FighterAbilityId.microjumpdrive:
        EffectId.fighter_ability_microjumpdrive,
    FighterAbilityId.dmg_boost:
        EffectId.fighter_damage_multiply,
    FighterAbilityId.evasion:
        EffectId.fighter_ability_evasive_maneuvers,
    FighterAbilityId.launch_bomb:
        EffectId.fighter_ability_launch_bomb,
    FighterAbilityId.kamikaze:
        EffectId.fighter_ability_kamikaze,
    FighterAbilityId.blaster_cannon_caldari:
        EffectId.fighter_ability_attack_m,
    FighterAbilityId.railgun_caldari:
        EffectId.fighter_ability_attack_m}
