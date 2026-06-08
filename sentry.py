from config import SCREEN_HEIGHT, SCREEN_WIDTH
from sentry_geometry import sentry_emitters
from shared import all_sprites, bullets
import pygame


class SentryBeam(pygame.sprite.Sprite):
    _image_sets = {}

    def __init__(self, center, damage, bullet_speed, beam_type="beam"):
        super().__init__()
        self.beam_type = beam_type
        self.images = self._get_images(beam_type)
        self.index = 0
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(midbottom=center)
        self.pos_y = float(self.rect.y)
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.last_update = pygame.time.get_ticks()

    @classmethod
    def _get_images(cls, beam_type):
        if beam_type not in cls._image_sets:
            cls._image_sets[beam_type] = [_build_sentry_beam_frame(frame, beam_type) for frame in range(3)]
        return cls._image_sets[beam_type]

    def update(self, pressed_keys=None, mouse_pos=None):
        if self.rect.bottom < 0:
            self.kill()
            return
        if pygame.time.get_ticks() - self.last_update > 60:
            self.index = (self.index + 1) % len(self.images)
            self.surf = self.images[self.index]
            self.last_update = pygame.time.get_ticks()

        self.pos_y -= self.bullet_speed
        self.rect.y = int(self.pos_y)


class SentryGun(pygame.sprite.Sprite):
    _image = None

    def __init__(self, index, count, lives, damage, bullet_speed, shot_interval_ms):
        super().__init__()
        self.surf = self._get_image()
        spacing = SCREEN_WIDTH / (count + 1)
        x = round(spacing * (index + 1))
        self.rect = self.surf.get_rect(midbottom=(x, SCREEN_HEIGHT - 8))
        self.max_lives = lives
        self.lives = lives
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.last_shot_time = 0
        self.last_hit_time = -10_000
        self.shot_interval_ms = shot_interval_ms
        self.damage_cooldown_ms = 420

    @classmethod
    def _get_image(cls):
        if cls._image is None:
            image = pygame.image.load("img/player/sentry_gun/sentry_gun_red.png").convert_alpha()
            cls._image = pygame.transform.scale(image, (48, 48))
        return cls._image

    def update(self, pressed_keys=None, mouse_pos=None):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < self.shot_interval_ms:
            return

        for beam_type, barrel_center in sentry_emitters(self.rect.left, self.rect.top, self.rect.width):
            beam = SentryBeam(barrel_center, self.damage, self.bullet_speed, beam_type)
            bullets.add(beam)
            all_sprites.add(beam)
        self.last_shot_time = now

    def take_damage(self, amount, now):
        if now - self.last_hit_time < self.damage_cooldown_ms:
            return False

        self.lives -= amount
        self.last_hit_time = now
        return self.lives <= 0


def _build_sentry_beam_frame(frame, beam_type):
    if beam_type == "laser":
        return _build_sentry_laser_frame(frame)

    surface = pygame.Surface((7, 34), pygame.SRCALPHA)
    red_alpha = 230 if frame != 1 else 200
    orange_alpha = 245 if frame == 1 else 220
    yellow_alpha = 255

    pygame.draw.rect(surface, (150, 16, 6, red_alpha), pygame.Rect(1, 1, 5, 32))
    pygame.draw.rect(surface, (255, 82, 16, orange_alpha), pygame.Rect(2, 2, 3, 30))
    pygame.draw.rect(surface, (255, 235, 56, yellow_alpha), pygame.Rect(3, 3, 1, 28))
    pygame.draw.rect(surface, (255, 248, 154, 210), pygame.Rect(2, 0, 3, 3))
    pygame.draw.rect(surface, (115, 8, 4, 190), pygame.Rect(0, 5, 1, 24))
    pygame.draw.rect(surface, (115, 8, 4, 190), pygame.Rect(6, 5, 1, 24))
    return surface


def _build_sentry_laser_frame(frame):
    surface = pygame.Surface((11, 44), pygame.SRCALPHA)
    edge_alpha = 230 if frame != 1 else 205
    core_alpha = 255

    pygame.draw.rect(surface, (16, 64, 128, edge_alpha), pygame.Rect(1, 2, 9, 40))
    pygame.draw.rect(surface, (44, 184, 255, 235), pygame.Rect(3, 1, 5, 42))
    pygame.draw.rect(surface, (212, 252, 255, core_alpha), pygame.Rect(5, 0, 1, 44))
    pygame.draw.rect(surface, (108, 226, 255, 220), pygame.Rect(4, 3, 3, 6))
    pygame.draw.rect(surface, (4, 24, 82, 190), pygame.Rect(0, 8, 1, 28))
    pygame.draw.rect(surface, (4, 24, 82, 190), pygame.Rect(10, 8, 1, 28))
    return surface
