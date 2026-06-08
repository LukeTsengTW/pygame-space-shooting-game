import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from explosion import HitSpark


class HitSparkTests(unittest.TestCase):
    def test_hit_spark_is_centered_on_impact(self):
        spark = HitSpark((123, 45), frame_delay=0)

        self.assertEqual(spark.rect.center, (123, 45))
        self.assertGreater(len(spark.images), 1)
        self.assertEqual(spark.surf.get_flags() & pygame.SRCALPHA, pygame.SRCALPHA)

    def test_hit_spark_uses_blue_laser_palette(self):
        spark = HitSpark((30, 40), frame_delay=0)
        first_frame = spark.images[0]
        colored_pixels = [
            first_frame.get_at((x, y))
            for x in range(first_frame.get_width())
            for y in range(first_frame.get_height())
            if first_frame.get_at((x, y)).a
        ]

        average_red = sum(color.r for color in colored_pixels) / len(colored_pixels)
        average_green = sum(color.g for color in colored_pixels) / len(colored_pixels)
        average_blue = sum(color.b for color in colored_pixels) / len(colored_pixels)

        self.assertGreater(average_blue, average_red)
        self.assertGreater(average_green, average_red)

    def test_hit_spark_advances_and_removes_itself(self):
        group = pygame.sprite.Group()
        spark = HitSpark((30, 40), frame_delay=0)
        group.add(spark)

        for _ in range(len(spark.images) + 1):
            group.update()

        self.assertFalse(spark.alive())


if __name__ == "__main__":
    unittest.main()
