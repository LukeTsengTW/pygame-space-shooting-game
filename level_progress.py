def can_select_level(requested_level, highest_unlocked_level):
    return 1 <= requested_level <= highest_unlocked_level


def unlocked_level_after_clear(highest_unlocked_level, cleared_level, final_level=15):
    next_level = min(cleared_level + 1, final_level)
    return max(highest_unlocked_level, next_level)
