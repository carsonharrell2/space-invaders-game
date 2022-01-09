import pygame
import sys

import json

from time import sleep

from bullet import Bullet
from alien import Alien


def add_high_score(stats):
    try:
        with open('high_score.json') as f:
            high_score = int(f.read())
    except ValueError:
        with open('high_score.json', 'w') as f:
            json.dump(stats.high_score, f)
    else:
        if stats.high_score > high_score:
            with open('high_score.json', 'w') as o:
                json.dump(stats.high_score, o)


def check_keydown_events(event, stats, ai_settings, screen, ship, bullets, aliens):
    """checks when a keyboard button is pressed"""
    if event.key == pygame.K_RIGHT:
        # moves the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # moves the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        add_high_score(stats)
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)


def check_keyup_events(event, ship):
    """checks when a keyboard button is released"""
    if event.key == pygame.K_RIGHT:
        # stop moving the ship
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # stop moving the ship
        ship.moving_left = False



def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """respond to events on the computer"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            add_high_score(stats)
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, stats,  ai_settings, screen, ship, bullets, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    restarts or starts the game from the beginning
    resets stats etc
    """
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    # prepare scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # empty groups
    aliens.empty()
    bullets.empty()

    # create fleet of aliens and center ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    ai_settings.initialize_dynamic_settings()


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """checks to see if play button and if so starts game"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """fill the screen and update it"""
    # redraw the screen
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """updates the position and quantity of the bullets"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # destroy bullets, create a new fleet, and reset the settings
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """fire a bullet"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_num_aliens(ai_settings, alien_width):
    """get number aliens on x axis"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """get number of rows on y axis"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """creates an alien"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """create a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_num_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """respond to ship being hit by an alien"""
    if stats.ships_left > 0:
        # decrement ships_left
        stats.ships_left -= 1

        sb.prep_ships()

        # empty everything
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """checks to see if the aliens have reached the bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """update the position of the aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_high_score(stats, sb):
    """check to see if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()