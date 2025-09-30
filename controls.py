import pygame

def handle_player_paddle_movement(player_paddle):
    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[pygame.K_LEFT]:
        player_paddle.rect.x -= player_paddle.movement_speed
    
    if pressed_keys[pygame.K_RIGHT]:
        player_paddle.rect.x += player_paddle.movement_speed

    if player_paddle.rect.x < 0:
        player_paddle.rect.x = 0
    elif player_paddle.rect.x > player_paddle.screen_width - player_paddle.rect.width:
        player_paddle.rect.x = player_paddle.screen_width - player_paddle.rect.width