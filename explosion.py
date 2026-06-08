import pygame

_HIT_SPARK_IMAGES = None


class HitSpark(pygame.sprite.Sprite):
    def __init__(self, center, frame_delay=35):
        super().__init__()
        self.images = _get_hit_spark_images()
        self.index = 0
        self.frame_delay = frame_delay
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()

    def update(self, pressed_keys=None, mouse_pos=None):
        if pygame.time.get_ticks() - self.last_update < self.frame_delay:
            return

        self.index += 1
        if self.index >= len(self.images):
            self.kill()
            return

        center = self.rect.center
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()


def _get_hit_spark_images():
    global _HIT_SPARK_IMAGES
    if _HIT_SPARK_IMAGES is None:
        _HIT_SPARK_IMAGES = _build_hit_spark_images()
    return _HIT_SPARK_IMAGES


def _build_hit_spark_images():
    frames = []
    size = 64
    center = size // 2
    arcs = [
        ((-19, -4), (-9, -13), (1, -6), (13, -16)),
        ((-17, 7), (-5, 12), (4, 5), (16, 12)),
        ((-5, -20), (1, -10), (9, -18), (18, -9)),
        ((-21, -12), (-13, -3), (-23, 5), (-11, 14)),
    ]
    particles = [(-22, -2), (-14, 16), (12, -18), (23, 4), (7, 19), (-5, -24)]

    for frame in range(6):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        progress = frame / 5
        core_alpha = max(0, 245 - frame * 28)
        glow_alpha = max(0, 150 - frame * 20)
        arc_alpha = max(0, 230 - frame * 34)
        ring_radius = 8 + frame * 5
        beam_half_width = max(1, 5 - frame // 2)

        pygame.draw.circle(surface, (34, 144, 255, glow_alpha), (center, center), 20 + frame * 3)
        pygame.draw.circle(surface, (61, 229, 255, max(0, 180 - frame * 24)), (center, center), ring_radius, 2)
        pygame.draw.circle(surface, (144, 245, 255, max(0, 120 - frame * 16)), (center, center), ring_radius + 7, 1)

        beam_top = center - 25 - frame * 2
        beam_bottom = center + 16 + frame
        pygame.draw.line(surface, (35, 194, 255, max(0, 150 - frame * 18)), (center, beam_top), (center, beam_bottom), beam_half_width + 6)
        pygame.draw.line(surface, (112, 244, 255, core_alpha), (center, beam_top + 3), (center, beam_bottom - 2), beam_half_width + 2)
        pygame.draw.line(surface, (247, 255, 255, core_alpha), (center, beam_top + 8), (center, center + 8), max(1, beam_half_width))

        pygame.draw.circle(surface, (88, 221, 255, 220), (center, center), max(3, 9 - frame))
        pygame.draw.circle(surface, (245, 255, 255, 250), (center, center), max(2, 5 - frame // 2))

        for arc_index, arc in enumerate(arcs):
            points = [
                (
                    center + int(x * (0.6 + progress * 0.7)),
                    center + int(y * (0.6 + progress * 0.7)),
                )
                for x, y in arc
            ]
            color = (90, 232, 255, arc_alpha) if arc_index % 2 else (40, 140, 255, arc_alpha)
            pygame.draw.lines(surface, color, False, points, max(1, 3 - frame // 2))

        for particle_index, (x, y) in enumerate(particles):
            drift = 0.45 + progress * 0.9 + particle_index * 0.03
            particle_pos = (center + int(x * drift), center + int(y * drift))
            particle_radius = max(1, 3 - frame // 2)
            pygame.draw.circle(surface, (131, 248, 255, arc_alpha), particle_pos, particle_radius)

        frames.append(surface)

    return frames


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, images):
        super().__init__()
        self.images = images
        self.index = 0 
        self.surf = self.images[self.index] 
        self.rect = self.surf.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()

    def update(self, pressed_keys=None, mouse_pos=None):
        if pygame.time.get_ticks() - self.last_update > 100: 
            self.index = (self.index + 1) % len(self.images) 
            self.surf = self.images[self.index] 
            self.last_update = pygame.time.get_ticks()
            if self.index == 0:
                self.kill()

class Explosion_1(Explosion):
    def __init__(self, center):
        images = []
        for i in range(1, 9):
            image = pygame.image.load(f'img/enemy/lv1_to_5/base/Scout_assets/Scout_frame_{i}.png').convert_alpha()
            if i in [1, 2]: 
                image = pygame.transform.scale(image, (37.4, 40.8))
            images.append(image)
        super().__init__(center, images)

class Explosion_2(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv1_to_5/base/Torpedo_assets/Torpedo_frame_{i}.png').convert_alpha() for i in range(1,9)]
        super().__init__(center, images)

class Explosion_3(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv1_to_5/base/Frigate_assets/Frigate_frame_{i}.png').convert_alpha() for i in range(1,9)]
        super().__init__(center, images)

class Explosion_4(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv1_to_5/base/Support_assets/Support_frame_{i}.png').convert_alpha() for i in range(1,9)]
        super().__init__(center, images)

class Explosion_5(Explosion):
    def __init__(self, center):
        images = []
        for i in range(1, 13):
            image = pygame.image.load(f'img/enemy/lv1_to_5/base/Battlecruiser_assets/Battlecruiser_frame_{i}.png').convert_alpha()
            if i <= 6:  # 只調整前6幀的大小
                image = pygame.transform.scale(image, (108, 132)) 
            images.append(image)
        super().__init__(center, images)

class Explosion_6(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv6_to_10/base/Scout_assets/Scout_frame_{i}.png').convert_alpha() for i in range(1,16)]
        super().__init__(center, images)

class Explosion_7(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv6_to_10/base/Torpedo_assets/Torpedo_frame_{i}.png').convert_alpha() for i in range(1,16)]
        super().__init__(center, images)

class Explosion_8(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv6_to_10/base/Frigate_assets/Frigate_frame_{i}.png').convert_alpha() for i in range(1,16)]
        super().__init__(center, images)

class Explosion_9(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv6_to_10/base/Support_assets/Support_frame_{i}.png').convert_alpha() for i in range(1,16)]
        super().__init__(center, images)

class Explosion_10(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv6_to_10/base/Battlecruiser_assets/Battlecruiser_frame_{i}.png').convert_alpha() for i in range(1,18)]
        super().__init__(center, images)

class Explosion_11(Explosion):
    def __init__(self, center):
        images = []
        for i in range(1, 18):
            image = pygame.image.load(f'img/enemy/lv6_to_10/base/Dreadnought_assets/Dreadnought_frame_{i}.png').convert_alpha()
            original_width, original_height = image.get_size()
            scaled_width = int(original_width * 1.5)
            scaled_height = int(original_height * 1.5)
            image = pygame.transform.scale(image, (scaled_width, scaled_height))
            images.append(image)
        super().__init__(center, images)

class Explosion_12(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Scout_assets/Scout_frame_{i}.png').convert_alpha() for i in range(1,10)]
        super().__init__(center, images)

class Explosion_13(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Bomber_assets/Bomber_frame_{i}.png').convert_alpha() for i in range(1,10)]
        super().__init__(center, images)

class Explosion_14(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Torpedo_assets/Torpedo_frame_{i}.png').convert_alpha() for i in range(1,8)]
        super().__init__(center, images)

class Explosion_15(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Frigate_assets/Frigate_frame_{i}.png').convert_alpha() for i in range(1,10)]
        super().__init__(center, images)

class Explosion_16(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Support_assets/Support_frame_{i}.png').convert_alpha() for i in range(1,8)]
        super().__init__(center, images)

class Explosion_17(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Battlecruiser_assets/Battlecruiser_frame_{i}.png').convert_alpha() for i in range(1,13)]
        super().__init__(center, images)

class Explosion_18(Explosion):
    def __init__(self, center):
        images = [pygame.image.load(f'img/enemy/lv11_to_15/base/Dreadnought_assets/Dreadnought_frame_{i}.png').convert_alpha() for i in range(1,13)]
        super().__init__(center, images)
