import unittest

import support_upgrades


class SupportUpgradeTests(unittest.TestCase):
    def test_next_upgrade_cost_increases_linearly_from_base_price(self):
        self.assertEqual(support_upgrades.next_upgrade_cost(50_000, 0), 50_000)
        self.assertEqual(support_upgrades.next_upgrade_cost(50_000, 1), 100_000)
        self.assertEqual(support_upgrades.next_upgrade_cost(50_000, 3), 200_000)
        self.assertEqual(support_upgrades.next_upgrade_cost(70_000, 3), 280_000)

    def test_sentry_gun_is_inactive_at_level_zero(self):
        stats = support_upgrades.sentry_gun_stats(0)
        self.assertIs(stats["active"], False)
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["bullet_speed"], 0)

    def test_sentry_gun_level_one_uses_base_stats(self):
        stats = support_upgrades.sentry_gun_stats(1)
        self.assertIs(stats["active"], True)
        self.assertEqual(stats["count"], 1)
        self.assertEqual(stats["lives"], 10)
        self.assertEqual(stats["damage"], 50)
        self.assertEqual(stats["bullet_speed"], 20)
        self.assertEqual(stats["shot_interval_ms"], 360)

    def test_sentry_gun_upgrades_stats_and_adds_units_every_five_levels(self):
        self.assertEqual(support_upgrades.sentry_gun_stats(4)["count"], 1)
        self.assertEqual(support_upgrades.sentry_gun_stats(5)["count"], 2)
        self.assertEqual(support_upgrades.sentry_gun_stats(10)["count"], 3)
        self.assertEqual(support_upgrades.sentry_gun_stats(15)["count"], 3)
        self.assertEqual(support_upgrades.sentry_gun_stats(3)["lives"], 14)
        self.assertEqual(support_upgrades.sentry_gun_stats(3)["damage"], 70)
        self.assertEqual(support_upgrades.sentry_gun_stats(3)["bullet_speed"], 26)
        self.assertEqual(support_upgrades.sentry_gun_stats(3)["shot_interval_ms"], 330)
        self.assertEqual(support_upgrades.sentry_gun_stats(30)["shot_interval_ms"], 25)

    def test_tactical_support_is_inactive_at_level_zero(self):
        stats = support_upgrades.tactical_support_stats(0)
        self.assertIs(stats["active"], False)

    def test_tactical_support_level_one_uses_base_trigger_and_cooldown(self):
        stats = support_upgrades.tactical_support_stats(1)
        self.assertIs(stats["active"], True)
        self.assertEqual(stats["trigger_ratio"], 0.30)
        self.assertEqual(stats["cooldown_ms"], 120_000)

    def test_tactical_support_improves_until_caps(self):
        self.assertEqual(support_upgrades.tactical_support_stats(3)["trigger_ratio"], 0.34)
        self.assertEqual(support_upgrades.tactical_support_stats(3)["cooldown_ms"], 116_000)
        self.assertEqual(support_upgrades.tactical_support_stats(30)["trigger_ratio"], 0.65)
        self.assertEqual(support_upgrades.tactical_support_stats(40)["cooldown_ms"], 60_000)

    def test_tactical_support_cooldown_can_be_reset_for_new_level(self):
        now = 200_000
        cooldown_ms = 120_000
        last_trigger_time = support_upgrades.reset_tactical_support_cooldown(now, cooldown_ms)
        self.assertTrue(
            support_upgrades.is_tactical_support_ready(now, last_trigger_time, cooldown_ms)
        )

    def test_tactical_support_effect_last_one_second(self):
        started_at = 50_000
        active_until = support_upgrades.tactical_support_active_until(started_at)
        self.assertEqual(active_until, 51_000)
        self.assertTrue(support_upgrades.is_tactical_support_effect_active(50_999, active_until))
        self.assertFalse(support_upgrades.is_tactical_support_effect_active(51_000, active_until))

    def test_tactical_support_targets_exclude_boss_groups(self):
        group_keys = ("enemies_1", "enemies_5", "enemies_11", "enemies_12", "enemies_18")
        boss_keys = ("enemies_5", "enemies_11", "enemies_18")
        self.assertEqual(
            support_upgrades.tactical_support_target_keys(group_keys, boss_keys),
            ("enemies_1", "enemies_12"),
        )


if __name__ == "__main__":
    unittest.main()
