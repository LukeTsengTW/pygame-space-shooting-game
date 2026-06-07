import sys
import random
from itertools import chain
from background import ScrollingBackground
from config import *
from enemy import Enemy, Enemy_1, Enemy_2, Enemy_3, Enemy_4, Enemy_5, Enemy_6, Enemy_7, Enemy_8, Enemy_9, Enemy_10, Enemy_11, Enemy_12, Enemy_13, Enemy_14, Enemy_15, Boss_1, Boss_2, Boss_3
from item import Item_1, Item_2
from explosion import Explosion_1, Explosion_2, Explosion_3, Explosion_4, Explosion_5, Explosion_6, Explosion_7, Explosion_8, Explosion_9, Explosion_10, Explosion_11, Explosion_12, Explosion_13, Explosion_14, Explosion_15, Explosion_16, Explosion_17, Explosion_18
from level_progress import can_select_level, unlocked_level_after_clear
from opening_skip import (
    OPENING_SKIP_PROMPT,
    OpeningSkipState,
    is_opening_skip_input,
)
from player import Player
from shared import enemy_bullets, enemies, all_sprites, bullets
from ui import (
    COLORS,
    create_creator_card,
    draw_button,
    draw_gameplay_hud,
    draw_heading,
    draw_modal_backdrop,
    draw_opening_briefing,
    draw_opening_skip_prompt as draw_ui_opening_skip_prompt,
    draw_panel,
    draw_slider,
    draw_stat_card,
    draw_tactical_starfield,
    draw_text as draw_ui_text,
    level_grid_rects,
)

items = {
    'item_1': pygame.sprite.Group(),
    'item_2': pygame.sprite.Group(),
}
enemies_p = {f"enemies_{i}": pygame.sprite.Group() for i in range(1, 19)}

level_start_time = 0

damage_level = 0
damage_level_need_coin = 0
bullet_speed_level = 0
bullet_speed_level_need_coin = 0
live_level = 0
live_level_need_coin = 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.display.set_caption('Space Shooter - Pygame Edition v1.0 - By: @LukeTseng')
font = pygame.font.Font('font.ttf', 36)
clock = pygame.time.Clock()

hard_level = 1
level = 1
highest_unlocked_level = level

is_complete_game = False

backgrounds = [pygame.image.load(f'img/background/lv{i}_background.jpg') for i in range(1, 21)]
gameplay_background = ScrollingBackground(backgrounds[0], speed=1)

score = 0 
running = True 

player = Player()
all_sprites.add(player)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def reset_game():
    for sprite in all_sprites:
        sprite.kill()

    all_sprites.add(player)
    player.lives = max_lives
    global score, level, level_start_time
    score, level = 0, 1
    level_start_time = pygame.time.get_ticks()

def reset_continue_game():
    for sprite in all_sprites:
        sprite.kill()

    all_sprites.add(player)
    player.lives = max_lives
    global score, level_start_time
    score = 0
    level_start_time = pygame.time.get_ticks()

current_text = 0 
def setting():
    global current_text, volume_level
    setting_running = True
    text_options = ['Control the sprite with keyboard', 'Control the sprite with cursor']

    control_button = pygame.Rect(90, 270, 420, 82)
    slider_rect = pygame.Rect(120, 490, 360, 18)
    back_button = pygame.Rect(180, 700, 240, 58)

    setting_background = ScrollingBackground(
        pygame.image.load('img/background/setting_background.jpg'),
        speed=2,
    )

    while setting_running:
        setting_background.advance()
        setting_background.draw(screen)

        mx, my = pygame.mouse.get_pos()
        draw_panel(screen, pygame.Rect(50, 145, 500, 655), alpha=232)
        draw_heading(screen, 'Settings', 'FLIGHT CONTROL CONFIGURATION', y=82)

        draw_ui_text(screen, 'CONTROL MODE', 16, COLORS['muted'], (90, 235), anchor='midleft')
        text = text_options[current_text]
        draw_button(
            screen,
            control_button,
            text,
            hovered=control_button.collidepoint((mx, my)),
            style='primary',
            subtitle='CLICK TO SWITCH INPUT SYSTEM',
        )

        draw_ui_text(screen, 'MASTER VOLUME', 16, COLORS['muted'], (90, 445), anchor='midleft')
        draw_slider(screen, slider_rect, volume_level)
        volume_percentage = f"{int(volume_level * 101)}%"
        draw_ui_text(screen, volume_percentage, 24, COLORS['text'], (SCREEN_WIDTH // 2, 545))
        draw_button(
            screen,
            back_button,
            'BACK TO MENU',
            hovered=back_button.collidepoint((mx, my)),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.buttons[0] == 1):
                if slider_rect.collidepoint((mx, my)):
                    volume_level = max(0.0, min(1.0, (mx - slider_rect.x) / slider_rect.width))
                    pygame.mixer.music.set_volume(volume_level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if control_button.collidepoint((mx, my)):
                        current_text = (current_text + 1) % len(text_options)
                        if current_text == 0:
                            player.control = 0
                        else:
                            player.control = 1
                    if back_button.collidepoint((mx, my)):
                        setting_running = False

        pygame.display.update()
        clock.tick(60)

def upgrade_UI():
    global BULLET_SPEED, max_lives, damage_level, bullet_speed_level, live_level, damage_level_need_coin, bullet_speed_level_need_coin, live_level_need_coin
    upgrade_UI_running = True

    upgrade_background = ScrollingBackground(
        pygame.image.load('img/background/upgrade_background.jpg'),
        speed=2,
    )

    while upgrade_UI_running:
        upgrade_background.advance()
        upgrade_background.draw(screen)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(75, 195, 450, 112)
        button_2 = pygame.Rect(75, 335, 450, 112)
        button_3 = pygame.Rect(75, 475, 450, 112)
        button_4 = pygame.Rect(180, 705, 240, 58)

        draw_panel(screen, pygame.Rect(45, 135, 510, 660), alpha=232)
        draw_heading(screen, 'Upgrade', 'SHIP SYSTEM ENHANCEMENT', y=76)
        draw_stat_card(
            screen,
            pygame.Rect(420, 45, 145, 64),
            'Coin',
            f'{player.coin:,}',
            accent=COLORS['gold'],
        )

        upgrade_rows = (
            (button_1, 'WEAPON DAMAGE', damage_level, damage_level_need_coin),
            (button_2, 'PROJECTILE SPEED', bullet_speed_level, bullet_speed_level_need_coin),
            (button_3, 'HULL CAPACITY', live_level, live_level_need_coin),
        )
        for button, label, upgrade_level, cost in upgrade_rows:
            affordable = player.coin >= cost
            draw_button(
                screen,
                button,
                f'{label}  /  LV.{upgrade_level}',
                hovered=button.collidepoint((mx, my)) and affordable,
                style='primary' if affordable else 'locked',
                disabled=not affordable,
                subtitle=f'COST  {cost:,} COINS',
            )

        draw_button(
            screen,
            button_4,
            'BACK TO MENU',
            hovered=button_4.collidepoint((mx, my)),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_1.collidepoint((mx, my)):
                        if player.coin >= damage_level_need_coin:
                            player.coin -= damage_level_need_coin
                            player.damage += 1
                            damage_level += 1
                            damage_level_need_coin = damage_level * 1234
                    if button_2.collidepoint((mx, my)):
                        if player.coin >= bullet_speed_level_need_coin:
                            player.coin -= bullet_speed_level_need_coin
                            BULLET_SPEED += 1
                            bullet_speed_level += 1
                            bullet_speed_level_need_coin = bullet_speed_level * 321
                            print("Bullet's speed is ", BULLET_SPEED, " now")
                    if button_3.collidepoint((mx, my)):
                        if player.coin >= live_level_need_coin:
                            player.coin -= live_level_need_coin
                            max_lives += 1
                            live_level += 1
                            live_level_need_coin = live_level * 5432
                            print("max_lives is ", max_lives, " now")
                    if button_4.collidepoint((mx, my)):
                        upgrade_UI_running = False

        pygame.display.update()
        clock.tick(60)

def credits():
    credits_running = True
    while credits_running:
        screen.fill(COLORS['navy'])
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(180, 790, 240, 58)
        draw_panel(screen, pygame.Rect(55, 130, 490, 630), alpha=240)
        draw_heading(screen, 'Credits', 'MISSION DEVELOPMENT CREW', y=72)

        credit_rows = (
            ('PROGRAMMER', 'LukeTseng'),
            ('GAME DESIGNER', 'LukeTseng'),
            ('GRAPH ARTIST / MATERIAL', 'FoozleCC'),
            ('BACKGROUND / MATERIAL', 'Leonardo AI'),
            ('MUSIC / MATERIAL', 'OpenGameArt : Oblidivm'),
            ('GAME ENGINE', 'Pygame'),
        )
        y = 190
        for role, name in credit_rows:
            draw_ui_text(screen, role, 14, COLORS['muted'], (SCREEN_WIDTH // 2, y))
            draw_ui_text(screen, name, 22, COLORS['text'], (SCREEN_WIDTH // 2, y + 28))
            y += 86

        draw_button(
            screen,
            button_1,
            'BACK',
            hovered=button_1.collidepoint((mx, my)),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_1.collidepoint((mx, my)):
                        credits_running = False

        pygame.display.update()
        clock.tick(60)

def chose_level():
    global level
    chose_level_running = True
    level_buttons = level_grid_rects(SCREEN_WIDTH, SCREEN_HEIGHT)
    button_back = pygame.Rect(180, 790, 240, 58)
    while chose_level_running:
        screen.fill(COLORS['navy'])
        mx, my = pygame.mouse.get_pos()
        draw_panel(screen, pygame.Rect(35, 150, 530, 590), alpha=235)
        draw_heading(screen, 'Mission Select', 'NORMAL CAMPAIGN', y=72)
        for index, button in enumerate(level_buttons, start=1):
            unlocked = can_select_level(index, highest_unlocked_level)
            draw_button(
                screen,
                button,
                f'LEVEL {index:02d}',
                hovered=unlocked and button.collidepoint((mx, my)),
                style='secondary' if unlocked else 'locked',
                disabled=not unlocked,
            )

        draw_button(
            screen,
            button_back,
            'BACK',
            hovered=button_back.collidepoint((mx, my)),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, button in enumerate(level_buttons, start=1):
                    if button.collidepoint((mx, my)):
                        if can_select_level(i, highest_unlocked_level):
                            play_music("music/battle_in_the_stars.ogg")
                            level = i
                            chose_level_running = False
                            player.out_of_game = False
                            reset_continue_game()
                            break
                if button_back.collidepoint((mx, my)):
                    chose_level_running = False
                    main_menu()
        pygame.display.update()
        clock.tick(60)

def chose_hard_level():
    global hard_level
    chose_hard_level_running = True
    level_buttons = level_grid_rects(SCREEN_WIDTH, SCREEN_HEIGHT)
    button_back = pygame.Rect(180, 790, 240, 58)
    while chose_hard_level_running:
        screen.fill(COLORS['navy'])
        mx, my = pygame.mouse.get_pos()
        draw_heading(screen, 'Hard Missions', 'ELITE CAMPAIGN', y=72)
        if is_complete_game:
            draw_panel(screen, pygame.Rect(35, 150, 530, 590), alpha=235)
            for i, button in enumerate(level_buttons, start=1):
                unlocked = i <= hard_level
                draw_button(
                    screen,
                    button,
                    f'LEVEL {i:02d}',
                    hovered=unlocked and button.collidepoint((mx, my)),
                    style='danger' if unlocked else 'locked',
                    disabled=not unlocked,
                )
        else:
            draw_panel(screen, pygame.Rect(70, 260, 460, 300), alpha=242)
            draw_ui_text(
                screen,
                'ACCESS DENIED',
                30,
                COLORS['danger_hover'],
                (SCREEN_WIDTH // 2, 350),
            )
            draw_ui_text(
                screen,
                'Complete the normal campaign',
                19,
                COLORS['text'],
                (SCREEN_WIDTH // 2, 420),
            )
            draw_ui_text(
                screen,
                'to unlock elite missions.',
                19,
                COLORS['muted'],
                (SCREEN_WIDTH // 2, 455),
            )

        draw_button(
            screen,
            button_back,
            'BACK',
            hovered=button_back.collidepoint((mx, my)),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, button in enumerate(level_buttons, start=1):
                    if button.collidepoint((mx, my)):
                        if is_complete_game and i <= hard_level:
                            hard_level = i
                            chose_hard_level_running = False
                            player.out_of_game = False
                            reset_continue_game()
                            break
                if button_back.collidepoint((mx, my)):
                    chose_hard_level_running = False
                    main_menu()
        pygame.display.update()
        clock.tick(60)

def main_menu():
    play_music("music/brave_pilots_menu_screen.ogg")
    main_running = True
    button_texts = ['Play', 'Upgrade', 'Setting', 'Exit', 'Credits', 'Hard Mode']
    button_actions = [chose_level, upgrade_UI, setting, sys.exit, credits, chose_hard_level]
    buttons = [
        pygame.Rect(155, 220 + i * 88, 290, 58)
        for i in range(len(button_texts))
    ]

    menu_background = ScrollingBackground(
        pygame.image.load('img/background/menu_background.jpg'),
        speed=2,
    )

    while main_running:
        menu_background.advance()
        menu_background.draw(screen)
        mx, my = pygame.mouse.get_pos()
        draw_panel(screen, pygame.Rect(115, 145, 370, 655), alpha=226, border=COLORS['cyan'])
        draw_heading(screen, 'Space Shooter', 'TACTICAL FLIGHT COMMAND', y=76)
        styles = ('primary', 'secondary', 'secondary', 'danger', 'secondary', 'secondary')
        for button, label, style in zip(buttons, button_texts, styles):
            draw_button(
                screen,
                button,
                label.upper(),
                hovered=button.collidepoint((mx, my)),
                style=style,
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for idx, button in enumerate(buttons):
                        if button.collidepoint((mx, my)):
                            if idx == 0 or idx == 5:
                                main_running = False
                            button_actions[idx]()

        pygame.display.update()
        clock.tick(60)

def game_over_screen():
    play_music('music/defeated_game_over_tune.ogg')
    game_over_running = True
    player.out_of_game = True
    pygame.mouse.set_visible(True)
    result_background = screen.copy()
    while game_over_running:
        screen.blit(result_background, (0, 0))
        modal = draw_modal_backdrop(screen, pygame.Rect(70, 225, 460, 450))
        draw_ui_text(screen, 'MISSION FAILED', 38, COLORS['danger_hover'], (modal.centerx, 315))
        draw_ui_text(
            screen,
            'Your ship has been destroyed.',
            18,
            COLORS['muted'],
            (modal.centerx, 375),
        )
        draw_button(
            screen,
            pygame.Rect(125, 445, 350, 62),
            '1  /  RETURN TO COMMAND',
            style='primary',
        )
        draw_button(
            screen,
            pygame.Rect(125, 535, 350, 62),
            '2  /  EXIT GAME',
            style='danger',
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main_menu()
                    game_over_running = False
                if event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

def all_levels_completed_screen():
    play_music('music/victory_tune.ogg')
    all_levels_completed_running = True
    player.out_of_game = True
    pygame.mouse.set_visible(True)
    result_background = screen.copy()
    while all_levels_completed_running:
        screen.blit(result_background, (0, 0))
        modal = draw_modal_backdrop(screen, pygame.Rect(60, 215, 480, 470))
        draw_ui_text(screen, 'CAMPAIGN COMPLETE', 34, COLORS['cyan_hover'], (modal.centerx, 305))
        draw_ui_text(
            screen,
            'All normal missions cleared.',
            19,
            COLORS['text'],
            (modal.centerx, 375),
        )
        draw_ui_text(
            screen,
            'Elite campaign access granted.',
            19,
            COLORS['gold'],
            (modal.centerx, 415),
        )
        draw_button(
            screen,
            pygame.Rect(120, 520, 360, 64),
            '1  /  RETURN TO COMMAND',
            style='primary',
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type is pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main_menu()
                    all_levels_completed_running = False

def pause_menu():
    pause_running = True
    paused_background = screen.copy()
    button_1 = pygame.Rect(155, 365, 290, 62)
    button_2 = pygame.Rect(155, 460, 290, 62)
    button_3 = pygame.Rect(155, 555, 290, 62)
    while pause_running:
        screen.blit(paused_background, (0, 0))
        mx, my = pygame.mouse.get_pos()
        draw_modal_backdrop(screen, pygame.Rect(95, 210, 410, 500))
        draw_ui_text(screen, 'MISSION PAUSED', 34, COLORS['text'], (SCREEN_WIDTH // 2, 290))
        draw_button(
            screen,
            button_1,
            'CONTINUE',
            hovered=button_1.collidepoint((mx, my)),
            style='primary',
        )
        draw_button(
            screen,
            button_2,
            'SETTINGS',
            hovered=button_2.collidepoint((mx, my)),
        )
        draw_button(
            screen,
            button_3,
            'BACK TO MENU',
            hovered=button_3.collidepoint((mx, my)),
            style='danger',
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_1.collidepoint((mx, my)):
                        pause_running = False
                        player.out_of_game = False
                    if button_2.collidepoint((mx, my)):
                        setting()
                    if button_3.collidepoint((mx, my)):
                        pause_running = False
                        main_menu()

        pygame.display.update()
        clock.tick(60)

def stage_clear_screen(level, score):
    global BOSS_1_GENERATION_ONCE, BOSS_2_GENERATION_ONCE
    BOSS_1_GENERATION_ONCE = False
    BOSS_2_GENERATION_ONCE = False
    stage_clear_running = True
    animation_score = 0
    animation_time = 0
    player.out_of_game = True
    pygame.mouse.set_visible(True)
    result_background = screen.copy()
    while stage_clear_running:
        screen.blit(result_background, (0, 0))
        draw_modal_backdrop(screen, pygame.Rect(65, 120, 470, 700))
        draw_ui_text(screen, 'MISSION COMPLETE', 34, COLORS['cyan_hover'], (SCREEN_WIDTH // 2, 205))
        draw_ui_text(screen, 'FINAL SCORE', 15, COLORS['muted'], (SCREEN_WIDTH // 2, 275))
        draw_ui_text(screen, f'{animation_score:,}', 34, COLORS['gold'], (SCREEN_WIDTH // 2, 320))

        if pygame.time.get_ticks() - animation_time > 5:
            if animation_score <= score:
                animation_score += 1
                animation_time = pygame.time.get_ticks()
        
        mx, my = pygame.mouse.get_pos()
        button_next_level = pygame.Rect(150, 390, 300, 58)
        button_restart_level = pygame.Rect(150, 470, 300, 58)
        button_back_menu = pygame.Rect(150, 690, 300, 58)
        draw_button(
            screen,
            button_next_level,
            'NEXT LEVEL',
            hovered=button_next_level.collidepoint((mx, my)),
            style='primary',
        )
        draw_button(
            screen,
            button_restart_level,
            'RESTART LEVEL',
            hovered=button_restart_level.collidepoint((mx, my)),
        )
        draw_button(
            screen,
            button_back_menu,
            'BACK TO MENU',
            hovered=button_back_menu.collidepoint((mx, my)),
            style='danger',
        )
        
        if level > 1:
            button_previous_level = pygame.Rect(150, 550, 300, 58)
            draw_button(
                screen,
                button_previous_level,
                'PREVIOUS LEVEL',
                hovered=button_previous_level.collidepoint((mx, my)),
            )
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_next_level.collidepoint((mx, my)):
                    # Enter Next level
                    if BOSS_GENERATION_ONCE["enemies_5"] or BOSS_GENERATION_ONCE["enemies_11"] or BOSS_GENERATION_ONCE["enemies_18"]:
                        play_music('music/battle_in_the_stars.ogg')
                    player.out_of_game = False
                    return 'next'
                if button_back_menu.collidepoint((mx, my)):
                    stage_clear_running = False
                    # Return menu
                    return 'menu'
                if level > 1 and button_previous_level.collidepoint((mx, my)):
                    # Return pervious level
                    if BOSS_GENERATION_ONCE["enemies_5"] or BOSS_GENERATION_ONCE["enemies_11"] or BOSS_GENERATION_ONCE["enemies_18"]:
                        play_music('music/battle_in_the_stars.ogg')
                    player.out_of_game = False
                    return 'previous'
                if button_restart_level.collidepoint((mx, my)):
                    # Restart current level
                    if BOSS_GENERATION_ONCE["enemies_5"] or BOSS_GENERATION_ONCE["enemies_11"] or BOSS_GENERATION_ONCE["enemies_18"]:
                        play_music('music/battle_in_the_stars.ogg')
                    player.out_of_game = False
                    return 'restart'

def check_bullet_hit(bullets, enemies, score_increment, drop_rate_1, drop_rate_2, Explosion, gain_coin=0):
    global score
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hit_enemies:
            bullet.kill()
            if not enemy.invincible:
                enemy.hp -= player.damage
                if enemy.hp <= 0:
                    boom_sound_effect.play()
                    player.coin += gain_coin
                    enemies.remove(enemy)
                    explosion = Explosion(enemy.rect.center)
                    all_sprites.add(explosion)
                    score += score_increment
                    if level >= 2:
                        if random.random() < drop_rate_1:
                            item1 = Item_1(enemy.rect.center)
                            items['item_1'].add(item1)
                            all_sprites.add(item1)
                    if level >= 4:
                        if random.random() < drop_rate_2:
                            item2 = Item_2(enemy.rect.center)
                            items['item_2'].add(item2)
                            all_sprites.add(item2)

def item_collision(player, item_type):
    hit_items = pygame.sprite.spritecollide(player, items[item_type], True)
    for item in hit_items:
        if item_type == 'item_1' and player.lives < max_lives:
            player.lives += 1
        elif item_type == 'item_2':
            player.activate_shield()          

def reset_enemies():
    for sprite in chain(*[enemies, *enemies_p.values(), enemy_bullets, items['item_1'], items['item_2']]):
        sprite.kill()
    
    BOSS_GENERATION_ONCE['enemies_5'] = False
    BOSS_GENERATION_ONCE['enemies_11'] = False
    BOSS_GENERATION_ONCE['enemies_18'] = False

last_spawn_time = 0

def generate_enemy(level, enemy_type, enemy_class, boss=False, Is_support=False):
    global last_spawn_time
    if boss:
        if not BOSS_GENERATION_ONCE[enemy_type]:
            boss = enemy_class()
            enemies_p[enemy_type].add(boss)
            all_sprites.add(boss)
            BOSS_GENERATION_ONCE[enemy_type] = True
            play_music('music/death_match_boss_theme.ogg')
    else:
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= 50 and random.random() < ENEMY_GENERATION_THRESHOLDS[enemy_type]:
            enemy = enemy_class(enemies) if Is_support else enemy_class()
            enemies_p[enemy_type].add(enemy)
            all_sprites.add(enemy)
            if not Is_support:
                enemies.add(enemy)
            last_spawn_time = current_time

def draw_health_bar(boss, screen):
    max_health = boss.maxhp
    current_health = boss.hp
    health_bar_length = 100  # Total length of the health bar
    current_health_length = (current_health / max_health) * health_bar_length
    health_bar_height = 10  # Height of the health bar
    # Adjust health bar position based on boss direction
    if boss.direction == 0:  # Right
        health_bar_x = boss.rect.right - health_bar_length
        health_bar_y = boss.rect.top - health_bar_height - 10
    elif boss.direction == 1:  # Down
        health_bar_x = boss.rect.left
        health_bar_y = boss.rect.bottom + 10
    elif boss.direction == 2:  # Left
        health_bar_x = boss.rect.left
        health_bar_y = boss.rect.top - health_bar_height - 10
    elif boss.direction == 3:  # Up
        health_bar_x = boss.rect.left
        health_bar_y = boss.rect.top - health_bar_height - 20
    pygame.draw.rect(screen, (255,0,0), (health_bar_x, health_bar_y, health_bar_length, health_bar_height))
    pygame.draw.rect(screen, (0,255,0), (health_bar_x, health_bar_y, current_health_length, health_bar_height))

def display_text(text, value, color, position):
    rendered_text = font.render('{}: {}'.format(text, value), True, color)
    screen.blit(rendered_text, position)

def draw_opening_skip_prompt(skip_state):
    if skip_state.prompt_visible:
        draw_ui_opening_skip_prompt(screen, OPENING_SKIP_PROMPT)


def process_opening_events(skip_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if is_opening_skip_input(
            event.type,
            pygame.KEYDOWN,
            pygame.MOUSEBUTTONDOWN,
        ) and skip_state.press_key():
            return True

    return False


def wait_during_opening(duration, skip_state, draw_frame):
    end_time = pygame.time.get_ticks() + duration
    while pygame.time.get_ticks() < end_time:
        if process_opening_events(skip_state):
            return True

        draw_frame()
        draw_opening_skip_prompt(skip_state)
        pygame.display.update()
        clock.tick(60)

    return False


def draw_opening_text(text, step, total_steps):
    draw_opening_briefing(
        screen,
        text,
        step,
        total_steps,
        pygame.time.get_ticks(),
    )


def display_text_word_by_word(text, step, total_steps, skip_state, delay=40):
    rendered_text = ''
    text_sound_effect.play()
    for word in text:
        rendered_text += word
        if wait_during_opening(
            delay,
            skip_state,
            lambda current_text=rendered_text: draw_opening_text(
                current_text,
                step,
                total_steps,
            ),
        ):
            text_sound_effect.stop()
            return True

    return False

def display_opening_screen(texts, delay=500):
    skip_state = OpeningSkipState()
    pygame.mixer.music.load('music/skyfire_title_screen.ogg')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.3)
    total_steps = len(texts)
    for step, text in enumerate(texts, start=1):
        if display_text_word_by_word(text, step, total_steps, skip_state):
            pygame.mixer.music.stop()
            return

        text_sound_effect.stop()
        if wait_during_opening(
            delay,
            skip_state,
            lambda current_text=text: draw_opening_text(
                current_text,
                step,
                total_steps,
            ),
        ):
            pygame.mixer.music.stop()
            return
    
    text_sound_effect.stop()
    creator_card = create_creator_card((440, 260))
    creator_rect = creator_card.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    for alpha in range(0, 256, 10):
        def draw_credit_fade_in(current_alpha=alpha):
            draw_tactical_starfield(screen, pygame.time.get_ticks())
            creator_card.set_alpha(current_alpha)
            screen.blit(creator_card, creator_rect)

        if wait_during_opening(100, skip_state, draw_credit_fade_in):
            pygame.mixer.music.stop()
            return
    
    def draw_credit():
        draw_tactical_starfield(screen, pygame.time.get_ticks())
        creator_card.set_alpha(255)
        screen.blit(creator_card, creator_rect)

    if wait_during_opening(3000, skip_state, draw_credit):
        pygame.mixer.music.stop()
        return

    for alpha in range(255, -1, -10):
        def draw_credit_fade_out(current_alpha=alpha):
            draw_tactical_starfield(screen, pygame.time.get_ticks())
            creator_card.set_alpha(current_alpha)
            screen.blit(creator_card, creator_rect)

        if wait_during_opening(100, skip_state, draw_credit_fade_out):
            pygame.mixer.music.stop()
            return

    if wait_during_opening(
        1000,
        skip_state,
        lambda: draw_tactical_starfield(screen, pygame.time.get_ticks()),
    ):
        pygame.mixer.music.stop()

texts = [
    'Earthlings from parallel universes', 
    'came to our current Earth.', 
    'Now, they are invading', 
    'and plundering our resources.', 
    'Enter the battleship, warrior.', 
    'We need your help and',
    'we can provide you with',
    'support and supplies',
    'You are the only hope',
    'for us people on earth.',
    'Go, you will be a hero.',
]

display_opening_screen(texts)

main_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(True)
                pause_menu()
    
    if pygame.time.get_ticks() - level_start_time > 3000:
        if level < 6:
            generate_enemy(level, 'enemies_1', Enemy_1)
            if level > 1:
                generate_enemy(level, 'enemies_2', Enemy_2)
            if level > 2:
                generate_enemy(level, 'enemies_3', Enemy_3)
            if level > 3:
                generate_enemy(level, 'enemies_4', Enemy_4, Is_support=True)
            if level == 5:
                generate_enemy(level, 'enemies_5', Boss_1, boss=True)
        elif level > 5 and level <= 10:
            generate_enemy(level, 'enemies_6', Enemy_5)
            generate_enemy(level, 'enemies_7', Enemy_6)
            if level > 6:
                generate_enemy(level, 'enemies_8', Enemy_7)
            if level > 7:
                generate_enemy(level, 'enemies_9', Enemy_8, Is_support=True)
                generate_enemy(level, 'enemies_10', Enemy_9)
            if level == 10:
                generate_enemy(level, 'enemies_11', Boss_2, boss=True)
        elif level > 10:
            generate_enemy(level, 'enemies_12', Enemy_10)
            generate_enemy(level, 'enemies_13', Enemy_11)
            if level > 11:
                generate_enemy(level, 'enemies_14', Enemy_12)
                generate_enemy(level, 'enemies_15', Enemy_13)
            if level > 12:
                generate_enemy(level, 'enemies_16', Enemy_14, Is_support=True)
                generate_enemy(level, 'enemies_17', Enemy_15) 
            if level == 15:
                generate_enemy(level, 'enemies_18', Boss_3, boss=True)

    screen.fill((0, 0, 0))

    pressed_keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    all_sprites.update(pressed_keys, mouse_pos)

    if level <= len(backgrounds):
        active_background = backgrounds[level - 1]
        if gameplay_background.surface is not active_background:
            gameplay_background.set_surface(active_background)

    gameplay_background.advance()
    gameplay_background.draw(screen)

    for boss in enemies_p['enemies_18']:
        draw_health_bar(boss, screen)

    for boss in enemies_p['enemies_11']:
        draw_health_bar(boss, screen)

    for boss in enemies_p['enemies_5']:
        max_health = boss.maxhp
        current_health = boss.hp
        health_bar_length = 100  # Total length of the health bar
        current_health_length = (current_health / max_health) * health_bar_length
        health_bar_height = 10  # Height of the health bar
        pygame.draw.rect(screen, (255,0,0), (boss.rect.x, boss.rect.bottom + 10, health_bar_length, health_bar_height))
        pygame.draw.rect(screen, (0,255,0), (boss.rect.x, boss.rect.bottom + 10, current_health_length, health_bar_height))

    for group in items.values():
        for item in group:
            screen.blit(item.surf, item.rect)

    for enemy_bullet in enemy_bullets:
        screen.blit(enemy_bullet.surf, enemy_bullet.rect)
    
    check_bullet_hit(bullets, enemies_p['enemies_1'], 2, 0.03, 0.01, Explosion_1, 10)
    check_bullet_hit(bullets, enemies_p['enemies_2'], 3, 0.03, 0.01, Explosion_2, 20)
    check_bullet_hit(bullets, enemies_p['enemies_3'], 4, 0.03, 0.01, Explosion_3, 30)
    check_bullet_hit(bullets, enemies_p['enemies_4'], 5, 0.03, 0.01, Explosion_4, 40)
    check_bullet_hit(bullets, enemies_p['enemies_5'], 200, 0.03, 0.01, Explosion_5, 10000)
    check_bullet_hit(bullets, enemies_p['enemies_6'], 6, 0.03, 0.01, Explosion_6, 50)
    check_bullet_hit(bullets, enemies_p['enemies_7'], 7, 0.03, 0.01, Explosion_7, 60)
    check_bullet_hit(bullets, enemies_p['enemies_8'], 8, 0.03, 0.01, Explosion_8, 70)
    check_bullet_hit(bullets, enemies_p['enemies_9'], 9, 0.03, 0.01, Explosion_9, 80)
    check_bullet_hit(bullets, enemies_p['enemies_10'], 10, 0.03, 0.01, Explosion_10, 90)
    check_bullet_hit(bullets, enemies_p['enemies_11'], 600, 0.03, 0.01, Explosion_11, 50000)
    check_bullet_hit(bullets, enemies_p['enemies_12'], 11, 0.03, 0.01, Explosion_12, 100)
    check_bullet_hit(bullets, enemies_p['enemies_13'], 12, 0.03, 0.01, Explosion_13, 110)
    check_bullet_hit(bullets, enemies_p['enemies_14'], 13, 0.03, 0.01, Explosion_14, 120)
    check_bullet_hit(bullets, enemies_p['enemies_15'], 14, 0.03, 0.01, Explosion_15, 130)
    check_bullet_hit(bullets, enemies_p['enemies_16'], 15, 0.03, 0.01, Explosion_16, 140)
    check_bullet_hit(bullets, enemies_p['enemies_17'], 16, 0.03, 0.01, Explosion_17, 150)
    check_bullet_hit(bullets, enemies_p['enemies_18'], 1000, 0.03, 0.01, Explosion_18, 100000)

    for item_type in items.keys():
        item_collision(player, item_type)

    enemy_damage_values = {
        'enemies_1': 1, 
        'enemies_2': 1, 
        'enemies_3': 2, 
        'enemies_4': 1, 
        'enemies_5': 5,
        'enemies_6': 1, 
        'enemies_7': 2, 
        'enemies_8': 3, 
        'enemies_9': 1, 
        'enemies_10': 3,
        'enemies_11': 5, 
        'enemies_12': 2,
        'enemies_13': 2,
        'enemies_14': 2,
        'enemies_15': 3,
        'enemies_16': 3,
        'enemies_17': 5,
        'enemies_18': 5,
    }

    enemy_groups = [(enemies_p[key], damage) for key, damage in enemy_damage_values.items()]
    for group, damage in enemy_groups:
        if pygame.sprite.spritecollideany(player, group):
            if not player.invincible and not player.invincible_shield:
                player.lives -= damage
                player.invincible = True
                player.last_hit_time = pygame.time.get_ticks()

    if pygame.sprite.spritecollideany(player, enemy_bullets):
        if not player.invincible and not player.invincible_shield:
            player.lives -= (level // 5 + 1)
            player.invincible = True 
            player.last_hit_time = pygame.time.get_ticks() 

    if player.invincible and pygame.time.get_ticks() - player.last_hit_time > 3000:
        player.invincible = False

    if player.invincible_shield and pygame.time.get_ticks() - player.shield_start_time > 5000:
        player.invincible_shield = False

    if player.lives <= 0:
        game_over_screen()
    
    if level > 15:
        all_levels_completed_screen()
        is_complete_game = True
    
    if score > 100 + (level * 10) * 9: # 100 + (level * 10) * 9
        action = stage_clear_screen(level, score)
        highest_unlocked_level = unlocked_level_after_clear(highest_unlocked_level, level)
        if action == 'next':
            reset_enemies()
            level += 1
            score = 0
            player.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
            player.lives = max_lives
            level_start_time = pygame.time.get_ticks()
        elif action == 'menu':
            main_menu()
        elif action == 'previous':
            reset_enemies()
            level -= 1
            score = 0
            player.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
            player.lives = max_lives
            level_start_time = pygame.time.get_ticks() 
        elif action == 'restart':
            reset_enemies()
            score = 0
            player.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
            player.lives = max_lives
            level_start_time = pygame.time.get_ticks() 

    for entity in all_sprites:
        if entity == player:
            player.draw(screen)
        else:
            screen.blit(entity.surf, entity.rect)

    for entity in all_sprites:
        if isinstance(entity, Enemy) and entity.invincible:
            if entity.shield_surf is not None:
                screen.blit(entity.shield_surf, entity.shield_rect)

    draw_gameplay_hud(screen, level, score, player.lives, player.coin)

    pygame.display.flip()
    clock.tick(180) 

pygame.quit()
sys.exit()
