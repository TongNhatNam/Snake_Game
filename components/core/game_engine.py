"""
Game Engine - Core game logic and main loop
"""

import pygame
import sys
from .config import config

class GameEngine:
    """Core game engine handling main loop and state management"""
    
    def __init__(self):
        try:
            pygame.init()
            self.screen_width, self.screen_height = config.get_screen_size()
            self.fps = config.get_fps()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Enhanced Snake Game")
            self.clock = pygame.time.Clock()
            
            # Game state
            self.state = "menu"
            self.running = True
            
            # Fonts with error handling
            try:
                self.font_large = pygame.font.Font(None, 60)
                self.font_medium = pygame.font.Font(None, 40)
                self.font_small = pygame.font.Font(None, 30)
            except pygame.error:
                default_font = pygame.font.get_default_font()
                self.font_large = pygame.font.Font(default_font, 60)
                self.font_medium = pygame.font.Font(default_font, 40)
                self.font_small = pygame.font.Font(default_font, 30)
        except Exception as e:
            raise RuntimeError(f"GameEngine initialization failed: {e}")
    
    def handle_quit(self):
        """Handle quit event"""
        self.running = False
    
    def update_screen_size(self):
        """Update screen size if changed in settings"""
        try:
            new_width, new_height = config.get_screen_size()
            if new_width != self.screen_width or new_height != self.screen_height:
                self.screen_width, self.screen_height = new_width, new_height
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                return True
            return False
        except Exception:
            return False
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Draw text on screen"""
        try:
            text_surface = font.render(str(text), True, color)
            if center:
                text_rect = text_surface.get_rect(center=(x, y))
            else:
                text_rect = text_surface.get_rect(topleft=(x, y))
            self.screen.blit(text_surface, text_rect)
        except Exception:
            pass
    
    def run(self):
        """Main game loop - to be implemented by subclass"""
        raise NotImplementedError("Subclass must implement run method")