import pygame
import sys
from components import PlayerPaddle, GameBall, GameUserInterface
from controls import handle_player_paddle_movement
from ui_manager import UIStateManager, GameState
from game_utils import (
    reset_ball_to_center_position, 
    create_brick_grid, 
    process_all_game_collisions,
    restart_game
)
from constants import (
    GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    PLAYER_PADDLE_WIDTH, PLAYER_PADDLE_HEIGHT, GAME_BALL_WIDTH, GAME_BALL_HEIGHT,
    UI_SCORE_FONT_SIZE, GAME_TARGET_FPS, PLAYER_INITIAL_LIVES,
    PLAYER_PADDLE_SPEED, PLAYER_PADDLE_Y_POSITION,
    BALL_INITIAL_HORIZONTAL_SPEED, BALL_INITIAL_VERTICAL_SPEED
)

pygame.init()

game_screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

all_game_sprites = pygame.sprite.Group()
brick_sprites = pygame.sprite.Group()

game_ui = GameUserInterface(GAME_SCREEN_WIDTH, COLOR_WHITE, UI_SCORE_FONT_SIZE)
ui_manager = UIStateManager(game_ui, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

player_paddle = PlayerPaddle(COLOR_WHITE, PLAYER_PADDLE_WIDTH, PLAYER_PADDLE_HEIGHT, 
                           GAME_SCREEN_WIDTH, PLAYER_PADDLE_SPEED, PLAYER_PADDLE_Y_POSITION)
all_game_sprites.add(player_paddle)

game_ball = GameBall(COLOR_WHITE, GAME_BALL_WIDTH, GAME_BALL_HEIGHT, COLOR_BLACK,
                    BALL_INITIAL_HORIZONTAL_SPEED, BALL_INITIAL_VERTICAL_SPEED)
game_ball.rect.x = GAME_SCREEN_WIDTH // 2
game_ball.rect.y = GAME_SCREEN_HEIGHT // 2
all_game_sprites.add(game_ball)

create_brick_grid(all_game_sprites, brick_sprites)

is_game_running = True
current_player_score = 0
remaining_player_lives = PLAYER_INITIAL_LIVES

game_clock = pygame.time.Clock()

while is_game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_game_running = False
            
            if ui_manager.current_state == GameState.START_SCREEN:
                if event.key == pygame.K_RETURN:
                    ui_manager.set_state(GameState.PLAYING)
            elif ui_manager.current_state in [GameState.PLAYING, GameState.PAUSED]:
                if event.key == pygame.K_SPACE:
                    ui_manager.toggle_pause()
            elif ui_manager.current_state == GameState.GAME_OVER or ui_manager.current_state == GameState.VICTORY:
                if event.key == pygame.K_r:
                    current_player_score, remaining_player_lives = restart_game(
                        game_ball, player_paddle, all_game_sprites, brick_sprites, ui_manager
                    )

    # Game logic (only when game is active and not paused)
    if ui_manager.current_state == GameState.PLAYING:
        handle_player_paddle_movement(player_paddle)
        all_game_sprites.update()
        points_earned_this_frame = process_all_game_collisions(game_ball, player_paddle, brick_sprites, GAME_SCREEN_WIDTH)
        current_player_score += points_earned_this_frame

        if game_ball.rect.bottom >= GAME_SCREEN_HEIGHT:
            remaining_player_lives -= 1
            if remaining_player_lives <= 0:
                ui_manager.set_state(GameState.GAME_OVER)
            else:
                reset_ball_to_center_position(game_ball, player_paddle)
            
        if not brick_sprites:
            ui_manager.set_state(GameState.VICTORY)

    ui_manager.render(game_screen, all_game_sprites, current_player_score, remaining_player_lives)

    pygame.display.flip()
    game_clock.tick(GAME_TARGET_FPS)

pygame.quit()
sys.exit()