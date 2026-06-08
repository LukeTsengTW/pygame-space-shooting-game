from config import SCREEN_HEIGHT, SCREEN_WIDTH
from shared import all_sprites, bullets
import pygame


class SentryBullet(pygame.sprite.Sprite):
    _images = None

    def __init__(self, origin_rect, damage, bullet_speed):
        super().__init__()
        self.images = self._get_images()
        self.index = 0
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(center=(origin_rect.centerx, origin_rect.top - 6))
        self.pos_y = float(self.rect.y)
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.last_update = pygame.time.get_ticks()

    @classmethod
    def _get_images(cls):
        if cls._images is None:
            cls._images = [
                pygame.transform.scale(
                    pygame.image.load(f"img/player/bullets/zapper_assets/zapper_frame_{i}.png"),
                    (5, 28),
                ).convert_alpha()
                for i in range(1, 9)
            ]
        return cls._images

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
            image = pygame.image.load("img/player/main_ship/full_health.png").convert_alpha()
            cls._image = pygame.transform.scale(image, (48, 48))
        return cls._image

    def update(self, pressed_keys=None, mouse_pos=None):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < self.shot_interval_ms:
            return

        bullet = SentryBullet(self.rect, self.damage, self.bullet_speed)
        bullets.add(bullet)
        all_sprites.add(bullet)
        self.last_shot_time = now

    def take_damage(self, amount, now):
        if now - self.last_hit_time < self.damage_cooldown_ms:
            return False

        self.lives -= amount
        self.last_hit_time = now
        return self.lives <= 0
