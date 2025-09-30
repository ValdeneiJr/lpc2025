import pygame
from enum import Enum


class GameState(Enum):
    START_SCREEN = "start_screen"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class UIStateManager:
    
    def __init__(self, game_ui, screen_width, screen_height):
        self.game_ui = game_ui
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_state = GameState.START_SCREEN
    
    def set_state(self, state):
        if isinstance(state, GameState):
            self.current_state = state
        else:
            raise ValueError(f"Invalid state: {state}. Must be a GameState enum value.")
    
    def get_state(self):
        return self.current_state
    
    def is_game_active(self):
        return self.current_state == GameState.PLAYING
    
    def is_game_paused(self):
        return self.current_state == GameState.PAUSED
    
    def is_start_screen(self):
        return self.current_state == GameState.START_SCREEN
    
    def is_game_over(self):
        return self.current_state == GameState.GAME_OVER
    
    def is_victory(self):
        return self.current_state == GameState.VICTORY
    
    def can_restart(self):
        return self.current_state in [GameState.GAME_OVER, GameState.VICTORY]
    
    def can_pause(self):
        return self.current_state == GameState.PLAYING
    
    def can_resume(self):
        return self.current_state == GameState.PAUSED
    
    def toggle_pause(self):
        if self.current_state == GameState.PLAYING:
            self.current_state = GameState.PAUSED
        elif self.current_state == GameState.PAUSED:
            self.current_state = GameState.PLAYING
        else:
            raise RuntimeError(f"Cannot toggle pause from state: {self.current_state}")
    
    def render(self, game_screen, all_sprites=None, score=0, lives=0):
        game_screen.fill((0, 0, 0))
        
        if self.current_state == GameState.START_SCREEN:
            self.game_ui.draw_start_screen(game_screen)
            
        elif self.current_state == GameState.PLAYING:
            if all_sprites:
                all_sprites.draw(game_screen)
            self.game_ui.draw_score_and_lives_display(game_screen, score, lives)
            self.game_ui.draw_pause_instruction(game_screen)
            
        elif self.current_state == GameState.PAUSED:
            if all_sprites:
                all_sprites.draw(game_screen)
            self.game_ui.draw_score_and_lives_display(game_screen, score, lives)
            self.game_ui.draw_pause_screen(game_screen)
            
        elif self.current_state == GameState.GAME_OVER:
            self.game_ui.draw_game_over_screen(game_screen, score)
            
        elif self.current_state == GameState.VICTORY:
            self.game_ui.draw_victory_screen(game_screen, score)
    
    def handle_key_input(self, key_event):
        actions = {
            'start_game': False,
            'restart_game': False,
            'toggle_pause': False,
            'quit_game': False
        }
        
        if key_event.type == pygame.KEYDOWN:
            if key_event.key == pygame.K_RETURN and self.is_start_screen():
                self.set_state(GameState.PLAYING)
                actions['start_game'] = True
                
            elif key_event.key == pygame.K_SPACE and (self.can_pause() or self.can_resume()):
                self.toggle_pause()
                actions['toggle_pause'] = True
                
            elif key_event.key == pygame.K_r and self.can_restart():
                self.set_state(GameState.PLAYING)
                actions['restart_game'] = True
                
            elif key_event.key == pygame.K_ESCAPE:
                actions['quit_game'] = True
        
        return actions