import unittest

from boss_health import (
    BossHealthDisplayState,
    get_boss_display_name,
    health_ratio,
)


class Boss_1:
    hp = 100
    maxhp = 100


class Boss_2:
    hp = 100
    maxhp = 100


class Boss_3:
    hp = 100
    maxhp = 100


class UnknownBoss:
    hp = 100
    maxhp = 100


class BossHealthMappingTests(unittest.TestCase):
    def test_boss_names_match_approved_level_names(self):
        self.assertEqual(get_boss_display_name(Boss_1()), "VOID CRUISER")
        self.assertEqual(get_boss_display_name(Boss_2()), "EARTH DESTROYER")
        self.assertEqual(get_boss_display_name(Boss_3()), "ANOTHER EARTHLING")

    def test_unknown_boss_uses_readable_fallback(self):
        self.assertEqual(get_boss_display_name(UnknownBoss()), "UNKNOWN BOSS")


class BossHealthRatioTests(unittest.TestCase):
    def test_health_ratio_clamps_into_visible_range(self):
        self.assertEqual(health_ratio(-10, 100), 0.0)
        self.assertEqual(health_ratio(0, 100), 0.0)
        self.assertEqual(health_ratio(50, 100), 0.5)
        self.assertEqual(health_ratio(150, 100), 1.0)

    def test_health_ratio_handles_invalid_max_health(self):
        self.assertEqual(health_ratio(100, 0), 0.0)
        self.assertEqual(health_ratio(100, -5), 0.0)


class BossHealthDisplayStateTests(unittest.TestCase):
    def test_new_boss_starts_without_damage_trail(self):
        boss = Boss_1()
        boss.hp = 80
        boss.maxhp = 100

        snapshot = BossHealthDisplayState().update(boss, 1000)

        self.assertEqual(snapshot.ratio, 0.8)
        self.assertEqual(snapshot.delayed_ratio, 0.8)

    def test_damage_trail_lingers_then_catches_up(self):
        boss = Boss_1()
        state = BossHealthDisplayState(damage_hold_ms=180, trail_speed_per_ms=0.0015)

        boss.hp = 100
        state.update(boss, 1000)
        boss.hp = 50

        immediate = state.update(boss, 1050)
        after_hold = state.update(boss, 1250)
        settled = state.update(boss, 2000)

        self.assertEqual(immediate.ratio, 0.5)
        self.assertEqual(immediate.delayed_ratio, 1.0)
        self.assertGreater(after_hold.delayed_ratio, after_hold.ratio)
        self.assertEqual(settled.delayed_ratio, settled.ratio)

    def test_healing_and_boss_swap_do_not_leave_delayed_bar_ahead(self):
        first = Boss_1()
        second = Boss_2()
        state = BossHealthDisplayState()

        first.hp = 20
        first_snapshot = state.update(first, 1000)
        first.hp = 90
        healed = state.update(first, 1100)
        second.hp = 40
        swapped = state.update(second, 1200)

        self.assertEqual(first_snapshot.delayed_ratio, 0.2)
        self.assertEqual(healed.delayed_ratio, healed.ratio)
        self.assertEqual(swapped.delayed_ratio, swapped.ratio)

    def test_none_resets_state_and_returns_none(self):
        boss = Boss_1()
        state = BossHealthDisplayState()

        self.assertIsNotNone(state.update(boss, 1000))
        self.assertIsNone(state.update(None, 1100))
        boss.hp = 35
        snapshot = state.update(boss, 1200)

        self.assertEqual(snapshot.delayed_ratio, snapshot.ratio)


if __name__ == "__main__":
    unittest.main()
