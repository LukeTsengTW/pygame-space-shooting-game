SENTRY_BARREL_X_RATIOS = (0.18, 0.31, 0.50, 0.69, 0.82)
SENTRY_EMITTER_TYPES = ("beam", "beam", "laser", "beam", "beam")
SENTRY_BARREL_Y_RATIO = 0.25


def sentry_barrel_centers(left, top, width):
    y = round(top + width * SENTRY_BARREL_Y_RATIO)
    return tuple((round(left + width * ratio), y) for ratio in SENTRY_BARREL_X_RATIOS)


def sentry_emitters(left, top, width):
    return tuple(zip(SENTRY_EMITTER_TYPES, sentry_barrel_centers(left, top, width)))
