"""Pure difficulty-scaling math for HARD MODE. No pygame/config imports so it
stays unit-testable in isolation (like level_progress.py). Callers pass the
live `config.is_enter_hard_mode` value as the `hard` argument."""

HARD_HP_MULTIPLIER = 3
HARD_DAMAGE_MULTIPLIER = 3
HARD_SPAWN_RATE_MULTIPLIER = 2
HARD_START_DELAY_FACTOR = 0.5
HARD_BOSS_COOLDOWN_FACTOR = 0.5


def scale_hp(base_hp, hard):
    return base_hp * HARD_HP_MULTIPLIER if hard else base_hp


def scale_damage(base_damage, hard):
    return base_damage * HARD_DAMAGE_MULTIPLIER if hard else base_damage


def scale_spawn_probability(probability, hard):
    return probability * HARD_SPAWN_RATE_MULTIPLIER if hard else probability


def scale_boss_cooldown(cooldown, hard):
    return int(cooldown * HARD_BOSS_COOLDOWN_FACTOR) if hard else cooldown


def scale_start_delay(delay, hard):
    return delay * HARD_START_DELAY_FACTOR if hard else delay
