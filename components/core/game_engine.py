"""
Game Engine - Core game logic and main loop
"""

import pygame
import sys
from .config import config

class GameEngine:
    """Core game engine handling main loop and state management"""
    
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = config.get_screen_size()
        self.fps = config.get_fps()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Enhanced Snake Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = "menu"
        self.running = True
        
        # Fonts
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
    
    def handle_quit(self):
        """Handle quit event"""
        self.running = False
    
    def update_screen_size(self):
        """Update screen size if changed in settings"""
        new_width, new_height = config.get_screen_size()
        if new_width != self.screen_width or new_height != self.screen_height:
            self.screen_width, self.screen_height = new_width, new_height
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            return True
        return False
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """Main game loop - to be implemented by subclass"""
        raise NotImplementedError("Subclass must implement run method")