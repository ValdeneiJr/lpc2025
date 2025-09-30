import pygame
import random
from components import GameBrick
from constants import (
    GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, BRICK_COLOR_PALETTE,
    BRICK_ELEMENT_WIDTH, BRICK_ELEMENT_HEIGHT, BRICK_GRID_ROWS, BRICK_GRID_COLUMNS,
    BRICK_LEFT_MARGIN, BRICK_TOP_MARGIN, BRICK_SPACING_DISTANCE,
    BALL_INITIAL_HORIZONTAL_SPEED, BALL_INITIAL_VERTICAL_SPEED
)


def reset_ball_to_center_position(game_ball, player_paddle):
    game_ball.rect.x = GAME_SCREEN_WIDTH // 2
    game_ball.rect.y = GAME_SCREEN_HEIGHT // 2
    
    horizontal_velocity = random.choice([
        -BALL_INITIAL_HORIZONTAL_SPEED, -BALL_INITIAL_HORIZONTAL_SPEED + 1, -BALL_INITIAL_HORIZONTAL_SPEED + 2, 
        BALL_INITIAL_HORIZONTAL_SPEED - 2, BALL_INITIAL_HORIZONTAL_SPEED - 1, BALL_INITIAL_HORIZONTAL_SPEED
    ])
    
    vertical_velocity = random.choice([
        -BALL_INITIAL_VERTICAL_SPEED, -BALL_INITIAL_VERTICAL_SPEED - 1, -BALL_INITIAL_VERTICAL_SPEED - 2
    ])
    
    game_ball.movement_velocity = [horizontal_velocity, vertical_velocity]


def create_brick_grid(all_game_sprites, brick_sprite_group):
    brick_point_values_per_row = [8, 8, 5, 5, 3, 3, 1, 1]

    for row_index in range(BRICK_GRID_ROWS):
        for column_index in range(BRICK_GRID_COLUMNS):
            brick_color_index = row_index % len(BRICK_COLOR_PALETTE)
            brick_point_value = brick_point_values_per_row[row_index]
            game_brick = GameBrick(BRICK_COLOR_PALETTE[brick_color_index], BRICK_ELEMENT_WIDTH, BRICK_ELEMENT_HEIGHT, brick_point_value)
            game_brick.rect.x = BRICK_LEFT_MARGIN + column_index * (BRICK_ELEMENT_WIDTH + BRICK_SPACING_DISTANCE)
            game_brick.rect.y = BRICK_TOP_MARGIN + row_index * (BRICK_ELEMENT_HEIGHT + BRICK_SPACING_DISTANCE)
            all_game_sprites.add(game_brick)
            brick_sprite_group.add(game_brick)


def handle_ball_wall_boundary_collisions(game_ball, screen_width):
    if game_ball.rect.left <= 0:
        game_ball.rect.left = 0
        game_ball.bounce_off_surface('x')
    elif game_ball.rect.right >= screen_width:
        game_ball.rect.right = screen_width
        game_ball.bounce_off_surface('x')

    if game_ball.rect.top <= 0:
        game_ball.rect.top = 0
        game_ball.bounce_off_surface('y')


def handle_ball_paddle_collision_detection(game_ball, player_paddle):
    if pygame.sprite.collide_rect(game_ball, player_paddle):
        if game_ball.movement_velocity[1] > 0:
            game_ball.rect.bottom = player_paddle.rect.top
            game_ball.bounce_off_surface('y')


def handle_ball_brick_collision_detection(game_ball, brick_sprite_group):
    collided_bricks = pygame.sprite.spritecollide(game_ball, brick_sprite_group, True)
    if collided_bricks:
        game_ball.bounce_off_surface('y')
        points_earned = sum(brick.point_value for brick in collided_bricks)
        return points_earned
    return 0


def process_all_game_collisions(game_ball, player_paddle, brick_sprite_group, screen_width):
    handle_ball_wall_boundary_collisions(game_ball, screen_width)
    handle_ball_paddle_collision_detection(game_ball, player_paddle)
    points_earned = handle_ball_brick_collision_detection(game_ball, brick_sprite_group)
    return points_earned


def restart_game(game_ball, player_paddle, all_game_sprites, brick_sprites, ui_manager):
    from constants import PLAYER_INITIAL_LIVES
    from ui_manager import GameState
    
    game_ball.rect.x = GAME_SCREEN_WIDTH // 2
    game_ball.rect.y = GAME_SCREEN_HEIGHT // 2
    game_ball.speed_x = BALL_INITIAL_HORIZONTAL_SPEED
    game_ball.speed_y = BALL_INITIAL_VERTICAL_SPEED
    
    brick_sprites.empty()
    all_game_sprites.empty()
    all_game_sprites.add(player_paddle)
    all_game_sprites.add(game_ball)
    create_brick_grid(all_game_sprites, brick_sprites)
    
    ui_manager.set_state(GameState.PLAYING)
    
    return 0, PLAYER_INITIAL_LIVES