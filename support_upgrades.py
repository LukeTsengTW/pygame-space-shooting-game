SENTRY_GUN_BASE_COST = 50_000
TACTICAL_SUPPORT_BASE_COST = 70_000

SENTRY_GUN_BASE_LIVES = 10
SENTRY_GUN_BASE_DAMAGE = 50
SENTRY_GUN_BASE_BULLET_SPEED = 20
SENTRY_GUN_BASE_SHOT_INTERVAL_MS = 360
SENTRY_GUN_LIVES_PER_LEVEL = 2
SENTRY_GUN_DAMAGE_PER_LEVEL = 10
SENTRY_GUN_BULLET_SPEED_PER_LEVEL = 3
SENTRY_GUN_SHOT_INTERVAL_REDUCTION_MS = 15
SENTRY_GUN_MIN_SHOT_INTERVAL_MS = 25
SENTRY_GUN_MAX_COUNT = 3

TACTICAL_SUPPORT_BASE_TRIGGER_RATIO = 0.30
TACTICAL_SUPPORT_MAX_TRIGGER_RATIO = 0.65
TACTICAL_SUPPORT_TRIGGER_RATIO_PER_LEVEL = 0.02
TACTICAL_SUPPORT_BASE_COOLDOWN_MS = 120_000
TACTICAL_SUPPORT_MIN_COOLDOWN_MS = 60_000
TACTICAL_SUPPORT_COOLDOWN_REDUCTION_MS = 2_000
TACTICAL_SUPPORT_EFFECT_DURATION_MS = 1_000


def next_upgrade_cost(base_cost, current_level):
    return int(base_cost * (max(0, current_level) + 1))


def sentry_gun_stats(level):
    level = max(0, int(level))
    if level <= 0:
        return {
            "active": False,
            "count": 0,
            "lives": 0,
            "damage": 0,
            "bullet_speed": 0,
            "shot_interval_ms": 0,
        }

    bonus_levels = level - 1
    return {
        "active": True,
        "count": min(SENTRY_GUN_MAX_COUNT, 1 + level // 5),
        "lives": SENTRY_GUN_BASE_LIVES + bonus_levels * SENTRY_GUN_LIVES_PER_LEVEL,
        "damage": SENTRY_GUN_BASE_DAMAGE + bonus_levels * SENTRY_GUN_DAMAGE_PER_LEVEL,
        "bullet_speed": SENTRY_GUN_BASE_BULLET_SPEED + bonus_levels * SENTRY_GUN_BULLET_SPEED_PER_LEVEL,
        "shot_interval_ms": max(
            SENTRY_GUN_MIN_SHOT_INTERVAL_MS,
            SENTRY_GUN_BASE_SHOT_INTERVAL_MS - bonus_levels * SENTRY_GUN_SHOT_INTERVAL_REDUCTION_MS,
        ),
    }


def tactical_support_stats(level):
    level = max(0, int(level))
    if level <= 0:
        return {
            "active": False,
            "trigger_ratio": 0.0,
            "cooldown_ms": 0,
        }

    bonus_levels = level - 1
    trigger_ratio = min(
        TACTICAL_SUPPORT_MAX_TRIGGER_RATIO,
        TACTICAL_SUPPORT_BASE_TRIGGER_RATIO + bonus_levels * TACTICAL_SUPPORT_TRIGGER_RATIO_PER_LEVEL,
    )
    cooldown_ms = max(
        TACTICAL_SUPPORT_MIN_COOLDOWN_MS,
        TACTICAL_SUPPORT_BASE_COOLDOWN_MS - bonus_levels * TACTICAL_SUPPORT_COOLDOWN_REDUCTION_MS,
    )
    return {
        "active": True,
        "trigger_ratio": round(trigger_ratio, 2),
        "cooldown_ms": cooldown_ms,
    }


def is_tactical_support_ready(now, last_trigger_time, cooldown_ms):
    return now - last_trigger_time >= cooldown_ms


def reset_tactical_support_cooldown(now, cooldown_ms):
    return now - cooldown_ms


def tactical_support_active_until(started_at):
    return started_at + TACTICAL_SUPPORT_EFFECT_DURATION_MS


def is_tactical_support_effect_active(now, active_until):
    return now < active_until


def tactical_support_target_keys(group_keys, boss_group_keys):
    boss_group_keys = set(boss_group_keys)
    return tuple(group_key for group_key in group_keys if group_key not in boss_group_keys)
