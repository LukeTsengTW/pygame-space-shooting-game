import unittest

from level_progress import can_select_level, unlocked_level_after_clear


class LevelProgressTests(unittest.TestCase):
    def test_selecting_an_earlier_level_does_not_change_the_unlock_limit(self):
        highest_unlocked_level = 10

        self.assertTrue(can_select_level(7, highest_unlocked_level))
        self.assertTrue(can_select_level(10, highest_unlocked_level))
        self.assertFalse(can_select_level(11, highest_unlocked_level))

    def test_clearing_an_earlier_level_does_not_reduce_progress(self):
        self.assertEqual(unlocked_level_after_clear(10, 7), 10)

    def test_clearing_the_latest_level_unlocks_the_next_level(self):
        self.assertEqual(unlocked_level_after_clear(10, 10), 11)

    def test_unlock_progress_is_capped_at_the_final_level(self):
        self.assertEqual(unlocked_level_after_clear(15, 15), 15)


if __name__ == "__main__":
    unittest.main()
