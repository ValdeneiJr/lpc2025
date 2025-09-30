import pygame

class PlayerPaddle(pygame.sprite.Sprite):
    def __init__(self, paddle_color, paddle_width, paddle_height, game_screen_width, 
                 movement_speed, y_position):
        super().__init__()

        self.image = pygame.Surface([paddle_width, paddle_height])
        self.image.fill(paddle_color)
        self.rect = self.image.get_rect()

        self.screen_width = game_screen_width
        self.movement_speed = movement_speed
        self.rect.x = (game_screen_width - paddle_width) / 2
        self.rect.y = y_position

class GameBall(pygame.sprite.Sprite):
    def __init__(self, ball_color, ball_width, ball_height, background_color, 
                 initial_horizontal_speed, initial_vertical_speed):
        super().__init__()

        self.image = pygame.Surface([ball_width, ball_height])
        self.image.fill(background_color)
        self.image.set_colorkey(background_color)

        pygame.draw.circle(self.image, ball_color, [ball_width // 2, ball_height // 2], ball_width // 2)

        self.rect = self.image.get_rect()
        self.movement_velocity = [initial_horizontal_speed, initial_vertical_speed]

    def update(self):
        self.rect.x += self.movement_velocity[0]
        self.rect.y += self.movement_velocity[1]

    def bounce_off_surface(self, bounce_axis):
        if bounce_axis == 'x':
            self.movement_velocity[0] = -self.movement_velocity[0]
        if bounce_axis == 'y':
            self.movement_velocity[1] = -self.movement_velocity[1]

class GameBrick(pygame.sprite.Sprite):
    def __init__(self, brick_color, brick_width, brick_height, point_value):
        super().__init__()

        self.image = pygame.Surface([brick_width, brick_height])
        self.image.fill(brick_color)
        self.rect = self.image.get_rect()
        self.point_value = point_value

class GameUserInterface:
    def __init__(self, game_screen_width, text_color, ui_font_size=36, title_font_size=74):
        self.screen_width = game_screen_width
        self.score_font = pygame.font.Font(None, ui_font_size)
        self.title_font = pygame.font.Font(None, title_font_size)
        self.text_color = text_color
        
    def draw_score_and_lives_display(self, game_screen, current_score, remaining_lives):
        score_text = self.score_font.render(f"Score: {current_score}", 1, self.text_color)
        game_screen.blit(score_text, (10, 10))
        
        lives_text = self.score_font.render(f"Lives: {remaining_lives}", 1, self.text_color)
        game_screen.blit(lives_text, (self.screen_width - 150, 10))
    
    def draw_game_over_screen(self, game_screen, final_score):
        game_over_text = self.title_font.render("GAME OVER", 1, self.text_color)
        screen_height = game_screen.get_height()
        game_screen.blit(game_over_text, (self.screen_width/2 - game_over_text.get_width()/2, screen_height/3))
        
        final_score_text = self.score_font.render(f"Final Score: {final_score}", 1, self.text_color)
        game_screen.blit(final_score_text, (self.screen_width/2 - final_score_text.get_width()/2, screen_height/3 + 50))
        
        restart_instruction_text = self.score_font.render("Press R to restart", 1, self.text_color)
        game_screen.blit(restart_instruction_text, (self.screen_width/2 - restart_instruction_text.get_width()/2, screen_height/3 + 100))
    
    def draw_victory_screen(self, game_screen, final_score):
        victory_text = self.title_font.render("YOU WIN!", 1, self.text_color)
        screen_height = game_screen.get_height()
        game_screen.blit(victory_text, (self.screen_width/2 - victory_text.get_width()/2, screen_height/3))
        
        final_score_text = self.score_font.render(f"Final Score: {final_score}", 1, self.text_color)
        game_screen.blit(final_score_text, (self.screen_width/2 - final_score_text.get_width()/2, screen_height/3 + 50))
        
        restart_instruction_text = self.score_font.render("Press R to restart", 1, self.text_color)
        game_screen.blit(restart_instruction_text, (self.screen_width/2 - restart_instruction_text.get_width()/2, screen_height/3 + 100))
    
    def draw_start_screen(self, game_screen):
        """Draw the initial start screen with game title and instructions."""
        title_text = self.title_font.render("BREAKOUT", 1, self.text_color)
        screen_height = game_screen.get_height()
        game_screen.blit(title_text, (self.screen_width/2 - title_text.get_width()/2, screen_height/3 - 50))
        
        start_instruction_text = self.score_font.render("Press ENTER to Play", 1, self.text_color)
        game_screen.blit(start_instruction_text, (self.screen_width/2 - start_instruction_text.get_width()/2, screen_height/3 + 50))
        
        controls_text = self.score_font.render("Use LEFT and RIGHT arrows to move paddle", 1, self.text_color)
        game_screen.blit(controls_text, (self.screen_width/2 - controls_text.get_width()/2, screen_height/3 + 100))
    
    def draw_pause_screen(self, game_screen):
        """Draw the pause screen overlay."""
        pause_text = self.title_font.render("PAUSED", 1, self.text_color)
        game_screen.blit(pause_text, (self.screen_width/2 - pause_text.get_width()/2, game_screen.get_height()/3))
        
        resume_instruction_text = self.score_font.render("Press SPACE to Resume", 1, self.text_color)
        game_screen.blit(resume_instruction_text, (self.screen_width/2 - resume_instruction_text.get_width()/2, game_screen.get_height()/3 + 80))
    
    def draw_pause_instruction(self, game_screen):
        gray_color = (128, 128, 128)
        pause_hint_font = pygame.font.Font(None, 24)
        pause_hint_text = pause_hint_font.render("Press SPACE to Pause", 1, gray_color)
        game_screen.blit(pause_hint_text, (self.screen_width - pause_hint_text.get_width() - 10, 
                                         game_screen.get_height() - 30))