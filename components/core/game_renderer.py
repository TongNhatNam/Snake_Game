"""
Game rendering system
"""

import pygame
from .config import config

class GameRenderer:
    """Handles all game rendering"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = config.get_screen_size()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_countdown(self, countdown_timer, countdown_duration):
        """Draw countdown screen"""
        self.screen.fill(config.get_color('background'))
        
        # Countdown text
        remaining_time = countdown_duration - countdown_timer
        if remaining_time > 2000:
            count_text = "3"
        elif remaining_time > 1000:
            count_text = "2"
        else:
            count_text = "1"
        
        # Animate countdown
        scale = 1.0 + 0.5 * (1.0 - (remaining_time % 1000) / 1000.0)
        font_size = int(100 * scale)
        font = pygame.font.Font(None, font_size)
        
        text_surface = font.render(count_text, True, config.get_color('text_highlight'))
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Instructions
        self.draw_text("Get Ready!", self.font_medium, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 100)
        self.draw_text("Press ESC to cancel", self.font_small, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 150)
    
    def draw_pause(self):
        """Draw pause screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(config.get_color('background'))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        self.draw_text("PAUSED", self.font_large, config.get_color('text_highlight'),
                      self.screen_width // 2, self.screen_height // 2 - 50)
        self.draw_text("Press SPACE to continue", self.font_medium, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 20)
        self.draw_text("Press ESC for main menu", self.font_medium, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 60)
    
    def draw_hud(self, score, level, lives, snake_move_interval, active_powerups, powerup_timers, game_area):
        """Draw heads-up display"""
        sidebar_x = game_area['x'] + game_area['width'] + 20
        
        # Score
        self.draw_text(f"Score: {score:06d}", self.font_medium, config.get_color('text'),
                      sidebar_x, 80, False)
        
        # Level
        self.draw_text(f"Level: {level}", self.font_medium, config.get_color('text'),
                      sidebar_x, 120, False)
        
        # Lives
        lives_text = "♥" * lives
        self.draw_text(f"Lives: {lives_text}", self.font_medium, config.get_color('text'),
                      sidebar_x, 160, False)
        
        # Speed
        speed_text = f"Speed: {int(1000/snake_move_interval):.1f}/sec"
        self.draw_text(speed_text, self.font_small, config.get_color('text'),
                      sidebar_x, 200, False)
        
        # Power-ups
        if active_powerups:
            self.draw_text("Power-ups:", self.font_small, config.get_color('text_highlight'),
                          sidebar_x, 240, False)
            y_offset = 260
            for k, v in powerup_timers.items():
                self.draw_text(f"{k}: {int(v/1000)}s", self.font_small, config.get_color('text'),
                              sidebar_x, y_offset, False)
                y_offset += 20
        
        # Instructions
        self.draw_text("Controls:", self.font_small, config.get_color('text_highlight'),
                      sidebar_x, 350, False)
        self.draw_text("WASD/Arrows: Move", self.font_small, config.get_color('text'),
                      sidebar_x, 370, False)
        self.draw_text("SPACE: Pause", self.font_small, config.get_color('text'),
                      sidebar_x, 390, False)
        self.draw_text("ESC: Menu", self.font_small, config.get_color('text'),
                      sidebar_x, 410, False)
    
    def draw_game(self, game_objects, game_state):
        """Draw game elements"""
        # Clear screen
        self.screen.fill(config.get_color('background'))
        
        # Draw game area border
        game_area = {
            'x': game_state.game_area_x,
            'y': game_state.game_area_y,
            'width': game_state.game_area_width,
            'height': game_state.game_area_height
        }
        
        game_rect = pygame.Rect(game_area['x']-2, game_area['y']-2, 
                               game_area['width']+4, game_area['height']+4)
        pygame.draw.rect(self.screen, (255, 255, 255), game_rect, 2)
        
        # Fill game area background
        game_bg = pygame.Rect(game_area['x'], game_area['y'], 
                             game_area['width'], game_area['height'])
        pygame.draw.rect(self.screen, (20, 20, 20), game_bg)
        
        # Draw game objects
        if 'obstacle_manager' in game_objects:
            game_objects['obstacle_manager'].draw(self.screen)
        if 'food_manager' in game_objects:
            game_objects['food_manager'].draw(self.screen)
        if 'powerup_manager' in game_objects:
            game_objects['powerup_manager'].draw(self.screen)
        if 'snake' in game_objects:
            game_objects['snake'].draw(self.screen)
        
        # Draw HUD
        if 'snake' in game_objects:
            snake = game_objects['snake']
            self.draw_hud(
                game_state.score, 
                game_state.level, 
                snake.get_lives(),
                game_state.snake_move_interval,
                snake.get_power_ups(),
                snake.get_power_up_timers(),
                game_area
            )