import unittest

from opening_skip import (
    OPENING_SKIP_PROMPT,
    OpeningSkipState,
    is_opening_skip_input,
)


class OpeningSkipStateTests(unittest.TestCase):
    def test_skip_prompt_is_english(self):
        self.assertEqual(OPENING_SKIP_PROMPT, "PRESS ANY KEY AGAIN TO SKIP")

    def test_keyboard_and_mouse_button_events_trigger_skip_input(self):
        keydown = 1
        mouse_button_down = 2

        self.assertTrue(is_opening_skip_input(keydown, keydown, mouse_button_down))
        self.assertTrue(
            is_opening_skip_input(mouse_button_down, keydown, mouse_button_down)
        )

    def test_other_events_do_not_trigger_skip_input(self):
        self.assertFalse(is_opening_skip_input(3, 1, 2))

    def test_first_key_press_reveals_prompt_without_skipping(self):
        state = OpeningSkipState()

        should_skip = state.press_key()

        self.assertFalse(should_skip)
        self.assertTrue(state.prompt_visible)
        self.assertFalse(state.skipped)

    def test_second_key_press_skips_the_opening(self):
        state = OpeningSkipState()
        state.press_key()

        should_skip = state.press_key()

        self.assertTrue(should_skip)
        self.assertTrue(state.skipped)

    def test_skip_request_remains_active_after_second_key_press(self):
        state = OpeningSkipState()
        state.press_key()
        state.press_key()

        self.assertTrue(state.press_key())


if __name__ == "__main__":
    unittest.main()
