from dataclasses import dataclass


BOSS_NAMES = {
    "Boss_1": "VOID CRUISER",
    "Boss_2": "EARTH DESTROYER",
    "Boss_3": "ANOTHER EARTHLING",
}


@dataclass(frozen=True)
class BossHealthSnapshot:
    name: str
    ratio: float
    delayed_ratio: float


def health_ratio(current, maximum):
    if maximum <= 0:
        return 0.0
    return max(0.0, min(1.0, current / maximum))


def get_boss_display_name(boss):
    if boss is None:
        return ""
    return BOSS_NAMES.get(boss.__class__.__name__, "UNKNOWN BOSS")


class BossHealthDisplayState:
    def __init__(self, *, damage_hold_ms=180, trail_speed_per_ms=0.0015):
        self.damage_hold_ms = damage_hold_ms
        self.trail_speed_per_ms = trail_speed_per_ms
        self._boss_id = None
        self._ratio = 0.0
        self._delayed_ratio = 0.0
        self._damage_started_ms = None
        self._damage_start_ratio = 0.0
        self._damage_target_ratio = 0.0

    def update(self, boss, now_ms):
        if boss is None:
            self.reset()
            return None

        boss_id = id(boss)
        ratio = health_ratio(getattr(boss, "hp", 0), getattr(boss, "maxhp", 0))

        if boss_id != self._boss_id:
            self._boss_id = boss_id
            self._ratio = ratio
            self._delayed_ratio = ratio
            self._damage_started_ms = None
            return BossHealthSnapshot(get_boss_display_name(boss), ratio, ratio)

        if ratio > self._ratio:
            self._ratio = ratio
            self._delayed_ratio = ratio
            self._damage_started_ms = None
            return BossHealthSnapshot(get_boss_display_name(boss), ratio, ratio)

        if ratio == self._ratio and self._damage_started_ms is None:
            return BossHealthSnapshot(
                get_boss_display_name(boss),
                ratio,
                self._delayed_ratio,
            )

        if self._damage_started_ms is None or ratio != self._damage_target_ratio:
            self._damage_started_ms = now_ms
            self._damage_start_ratio = max(self._delayed_ratio, self._ratio)
            self._damage_target_ratio = ratio

        self._ratio = ratio
        elapsed_ms = max(0, now_ms - self._damage_started_ms - self.damage_hold_ms)
        reduction = elapsed_ms * self.trail_speed_per_ms
        self._delayed_ratio = max(ratio, self._damage_start_ratio - reduction)

        return BossHealthSnapshot(
            get_boss_display_name(boss),
            ratio,
            self._delayed_ratio,
        )

    def reset(self):
        self._boss_id = None
        self._ratio = 0.0
        self._delayed_ratio = 0.0
        self._damage_started_ms = None
        self._damage_start_ratio = 0.0
        self._damage_target_ratio = 0.0
