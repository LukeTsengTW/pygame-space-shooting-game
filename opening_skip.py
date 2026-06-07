def is_opening_skip_input(event_type, keydown_type, mouse_button_down_type):
    return event_type in (keydown_type, mouse_button_down_type)


class OpeningSkipState:
    def __init__(self):
        self.prompt_visible = False
        self.skipped = False

    def press_key(self):
        if self.prompt_visible:
            self.skipped = True
        else:
            self.prompt_visible = True

        return self.skipped
