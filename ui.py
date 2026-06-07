from functools import lru_cache

import pygame


COLORS = {
    "navy": (5, 12, 23),
    "panel": (10, 25, 40),
    "panel_light": (17, 43, 63),
    "border": (48, 91, 116),
    "cyan": (70, 211, 247),
    "cyan_hover": (139, 235, 255),
    "cyan_dark": (13, 88, 115),
    "text": (230, 246, 255),
    "muted": (133, 164, 183),
    "gold": (255, 203, 92),
    "danger": (185, 65, 76),
    "danger_hover": (231, 92, 103),
    "locked": (55, 70, 82),
    "locked_text": (106, 126, 139),
    "track": (20, 43, 58),
}

FONT_PATH = "font.ttf"


@lru_cache(maxsize=None)
def get_font(size):
    return pygame.font.Font(FONT_PATH, size)


def level_grid_rects(screen_width, screen_height):
    button_width = 150
    button_height = 58
    column_gap = 20
    row_gap = 18
    columns = 3
    rows = 5
    grid_width = button_width * columns + column_gap * (columns - 1)
    grid_height = button_height * rows + row_gap * (rows - 1)
    start_x = (screen_width - grid_width) // 2
    start_y = max(190, (screen_height - grid_height) // 2 - 10)

    return [
        pygame.Rect(
            start_x + column * (button_width + column_gap),
            start_y + row * (button_height + row_gap),
            button_width,
            button_height,
        )
        for row in range(rows)
        for column in range(columns)
    ]


def gameplay_hud_rects(screen_width):
    widths = (106, 132, 106, 132)
    gap = 8
    total_width = sum(widths) + gap * (len(widths) - 1)
    x = (screen_width - total_width) // 2
    rects = []

    for width in widths:
        rects.append(pygame.Rect(x, 14, width, 62))
        x += width + gap

    return rects


def cut_corner_points(rect, cut=10):
    cut = max(0, min(cut, rect.width // 3, rect.height // 3))
    return [
        (rect.left + cut, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom - cut),
        (rect.right - cut, rect.bottom),
        (rect.left, rect.bottom),
        (rect.left, rect.top + cut),
    ]


def draw_text(
    surface,
    text,
    size,
    color,
    position,
    *,
    anchor="center",
):
    rendered = get_font(size).render(str(text), True, color)
    rect = rendered.get_rect()
    setattr(rect, anchor, position)
    surface.blit(rendered, rect)
    return rect


def draw_panel(
    surface,
    rect,
    *,
    fill=None,
    border=None,
    alpha=218,
    cut=12,
    border_width=2,
):
    rect = pygame.Rect(rect)
    fill = fill or COLORS["panel"]
    border = border or COLORS["border"]
    overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
    local_rect = overlay.get_rect()
    points = cut_corner_points(local_rect, cut)
    pygame.draw.polygon(overlay, (*fill, alpha), points)
    pygame.draw.lines(overlay, (*border, min(255, alpha + 25)), True, points, border_width)
    surface.blit(overlay, rect.topleft)
    return rect


def _button_colors(style, hovered, disabled):
    if disabled or style == "locked":
        return COLORS["locked"], COLORS["border"], COLORS["locked_text"]
    if style == "primary":
        fill = COLORS["cyan_dark"] if not hovered else (21, 119, 148)
        return fill, COLORS["cyan_hover"] if hovered else COLORS["cyan"], COLORS["text"]
    if style == "danger":
        fill = COLORS["danger_hover"] if hovered else COLORS["danger"]
        return fill, COLORS["danger_hover"], COLORS["text"]
    fill = COLORS["panel_light"] if hovered else COLORS["panel"]
    border = COLORS["cyan"] if hovered else COLORS["border"]
    return fill, border, COLORS["text"]


def draw_button(
    surface,
    rect,
    label,
    *,
    hovered=False,
    style="secondary",
    disabled=False,
    subtitle=None,
):
    rect = pygame.Rect(rect)
    fill, border, text_color = _button_colors(style, hovered, disabled)

    if hovered and not disabled:
        glow_rect = rect.inflate(8, 8)
        draw_panel(
            surface,
            glow_rect,
            fill=COLORS["navy"],
            border=border,
            alpha=110,
            cut=12,
            border_width=1,
        )

    draw_panel(surface, rect, fill=fill, border=border, alpha=238, cut=10)
    if subtitle:
        draw_text(
            surface,
            label,
            21,
            text_color,
            (rect.left + 18, rect.centery - 10),
            anchor="midleft",
        )
        draw_text(
            surface,
            subtitle,
            14,
            COLORS["muted"] if not disabled else COLORS["locked_text"],
            (rect.left + 18, rect.centery + 15),
            anchor="midleft",
        )
    else:
        draw_text(surface, label, 22, text_color, rect.center)
    return rect


def draw_heading(surface, title, subtitle=None, *, y=88):
    draw_text(surface, title.upper(), 38, COLORS["text"], (surface.get_width() // 2, y))
    accent_width = min(260, max(100, len(title) * 13))
    pygame.draw.line(
        surface,
        COLORS["cyan"],
        (surface.get_width() // 2 - accent_width // 2, y + 31),
        (surface.get_width() // 2 + accent_width // 2, y + 31),
        2,
    )
    if subtitle:
        draw_text(
            surface,
            subtitle,
            16,
            COLORS["muted"],
            (surface.get_width() // 2, y + 55),
        )


def draw_stat_card(surface, rect, label, value, *, accent=None):
    rect = pygame.Rect(rect)
    accent = accent or COLORS["cyan"]
    draw_panel(surface, rect, alpha=225, cut=8, border=accent, border_width=1)
    pygame.draw.line(
        surface,
        accent,
        (rect.left + 1, rect.top + 10),
        (rect.left + 1, rect.bottom - 2),
        3,
    )
    draw_text(
        surface,
        label.upper(),
        12,
        COLORS["muted"],
        (rect.left + 12, rect.top + 17),
        anchor="midleft",
    )
    draw_text(
        surface,
        value,
        21,
        accent if label.lower() == "coin" else COLORS["text"],
        (rect.left + 12, rect.bottom - 17),
        anchor="midleft",
    )
    return rect


def draw_gameplay_hud(surface, level, score, lives, coin):
    values = (
        ("Level", level, COLORS["cyan"]),
        ("Score", f"{score:,}", COLORS["cyan"]),
        ("Lives", lives, COLORS["cyan_hover"]),
        ("Coin", f"{coin:,}", COLORS["gold"]),
    )
    rects = gameplay_hud_rects(surface.get_width())
    for rect, (label, value, accent) in zip(rects, values):
        draw_stat_card(surface, rect, label, value, accent=accent)
    return rects


def draw_slider(surface, rect, value):
    rect = pygame.Rect(rect)
    value = max(0.0, min(1.0, value))
    pygame.draw.rect(surface, COLORS["track"], rect, border_radius=rect.height // 2)
    fill_rect = rect.copy()
    fill_rect.width = max(rect.height, round(rect.width * value))
    pygame.draw.rect(surface, COLORS["cyan"], fill_rect, border_radius=rect.height // 2)
    pygame.draw.rect(surface, COLORS["border"], rect, 2, border_radius=rect.height // 2)

    handle = pygame.Rect(0, 0, rect.height + 14, rect.height + 14)
    handle.center = (rect.left + round(rect.width * value), rect.centery)
    pygame.draw.circle(surface, COLORS["panel"], handle.center, handle.width // 2)
    pygame.draw.circle(surface, COLORS["cyan_hover"], handle.center, handle.width // 2, 3)
    return handle


def draw_modal_backdrop(surface, rect=None):
    shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    shade.fill((*COLORS["navy"], 210))
    surface.blit(shade, (0, 0))
    if rect is None:
        rect = pygame.Rect(70, 170, surface.get_width() - 140, surface.get_height() - 340)
    draw_panel(surface, rect, alpha=242, cut=16, border=COLORS["cyan"])
    return pygame.Rect(rect)


def draw_tactical_starfield(surface, tick):
    surface.fill(COLORS["navy"])
    width, height = surface.get_size()
    drift = tick // 35

    for index in range(72):
        x = (index * 83 + 29) % width
        y = (index * 137 + drift * (1 + index % 3)) % height
        brightness = 95 + (index * 31) % 130
        radius = 2 if index % 11 == 0 else 1
        pygame.draw.circle(
            surface,
            (brightness, min(255, brightness + 25), 255),
            (x, y),
            radius,
        )

    glow = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.circle(
        glow,
        (*COLORS["cyan_dark"], 38),
        (width // 2, height // 2),
        min(width, height) // 2,
    )
    surface.blit(glow, (0, 0))
    return surface.get_rect()


def draw_opening_briefing(surface, text, step, total_steps, tick):
    draw_tactical_starfield(surface, tick)
    width, height = surface.get_size()
    panel = pygame.Rect(55, 255, width - 110, 360)
    draw_panel(surface, panel, alpha=236, cut=16, border=COLORS["cyan"])

    draw_text(surface, "MISSION BRIEFING", 28, COLORS["text"], (width // 2, 105))
    draw_text(
        surface,
        "SECURE CHANNEL // EARTH COMMAND",
        14,
        COLORS["cyan"],
        (width // 2, 145),
    )
    pygame.draw.line(
        surface,
        COLORS["border"],
        (95, 180),
        (width - 95, 180),
        1,
    )

    scan_y = panel.top + 22 + (tick // 12) % (panel.height - 44)
    scan_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(
        scan_layer,
        (*COLORS["cyan"], 55),
        (panel.left + 18, scan_y),
        (panel.right - 18, scan_y),
        2,
    )
    surface.blit(scan_layer, (0, 0))

    draw_text(
        surface,
        "INCOMING TRANSMISSION",
        13,
        COLORS["muted"],
        (panel.left + 30, panel.top + 45),
        anchor="midleft",
    )
    draw_text(
        surface,
        text,
        24,
        COLORS["text"],
        panel.center,
    )

    safe_total = max(1, total_steps)
    safe_step = max(1, min(step, safe_total))
    progress_rect = pygame.Rect(panel.left + 30, panel.bottom - 62, panel.width - 60, 8)
    pygame.draw.rect(surface, COLORS["track"], progress_rect, border_radius=4)
    fill_rect = progress_rect.copy()
    fill_rect.width = max(8, round(progress_rect.width * safe_step / safe_total))
    pygame.draw.rect(surface, COLORS["cyan"], fill_rect, border_radius=4)
    draw_text(
        surface,
        f"PACKET {safe_step:02d} / {safe_total:02d}",
        13,
        COLORS["muted"],
        (panel.right - 30, panel.bottom - 28),
        anchor="midright",
    )
    return panel


def draw_opening_skip_prompt(surface, prompt):
    rect = pygame.Rect(115, surface.get_height() - 86, surface.get_width() - 230, 44)
    draw_panel(surface, rect, alpha=226, cut=8, border=COLORS["cyan"], border_width=1)
    draw_text(surface, prompt, 14, COLORS["cyan_hover"], rect.center)
    return rect


def create_creator_card(size):
    card = pygame.Surface(size, pygame.SRCALPHA)
    rect = card.get_rect().inflate(-4, -4)
    draw_panel(card, rect, alpha=242, cut=16, border=COLORS["cyan"])
    draw_text(card, "DEVELOPED BY", 15, COLORS["muted"], (rect.centerx, 58))
    draw_text(card, "LukeTseng", 36, COLORS["text"], (rect.centerx, 118))
    pygame.draw.line(
        card,
        COLORS["cyan"],
        (rect.left + 70, 157),
        (rect.right - 70, 157),
        2,
    )
    draw_text(card, "PYGAME EDITION", 15, COLORS["cyan"], (rect.centerx, 198))
    return card
