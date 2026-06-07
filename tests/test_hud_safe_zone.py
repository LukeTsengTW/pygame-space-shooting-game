import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from config import BOSS_BAR_HEIGHT, GAMEPLAY_TOP, HUD_HEIGHT


class SafeZoneConstantTests(unittest.TestCase):
    def test_safe_zone_constants_match_design(self):
        self.assertEqual(HUD_HEIGHT, 52)
        self.assertEqual(BOSS_BAR_HEIGHT, 30)
        self.assertEqual(GAMEPLAY_TOP, 82)


class GameplayEntitySafeZoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_player_cannot_move_above_gameplay_top_with_keyboard(self):
        from player import Player

        player = Player()
        player.out_of_game = False
        player.control = 0
        player.rect.top = GAMEPLAY_TOP - 12
        pressed = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

        player.update(pressed, player.rect.center)

        self.assertEqual(player.rect.top, GAMEPLAY_TOP)

    def test_player_mouse_control_clamps_to_gameplay_top(self):
        from player import Player

        player = Player()
        player.out_of_game = False
        player.control = 1

        player.update({}, (300, 10))

        self.assertEqual(player.rect.top, GAMEPLAY_TOP)

    def test_regular_enemy_spawns_inside_gameplay_area(self):
        from enemy import Enemy_1

        enemy = Enemy_1()

        self.assertGreaterEqual(enemy.rect.top, GAMEPLAY_TOP)

    def test_bosses_spawn_inside_gameplay_area(self):
        from enemy import Boss_1, Boss_2, Boss_3

        for boss_class in (Boss_1, Boss_2, Boss_3):
            boss = boss_class()

            self.assertGreaterEqual(boss.rect.top, GAMEPLAY_TOP)

    def test_boss_edge_path_uses_gameplay_top(self):
        from enemy import Boss_2, Boss_3

        for boss_class in (Boss_2, Boss_3):
            boss = boss_class()
            boss.move_phase = 3
            boss.rect.top = GAMEPLAY_TOP

            boss.move_sideways()

            self.assertEqual(boss.move_phase, 0)
            self.assertEqual(boss.direction, 1)

    def test_boss_upward_movement_does_not_overshoot_into_hud(self):
        from enemy import Boss_2, Boss_3

        for boss_class in (Boss_2, Boss_3):
            boss = boss_class()
            boss.move_phase = 3
            boss.rect.top = GAMEPLAY_TOP + 1

            boss.move_sideways()

            self.assertGreaterEqual(boss.rect.top, GAMEPLAY_TOP)


if __name__ == "__main__":
    unittest.main()
