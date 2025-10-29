"""
Base Menu class for all menu screens
"""

import pygame
from ..core import config

class Menu:
    """Base menu class"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = config.get_screen_size()
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        
        # Colors
        self.text_color = config.get_color('text')
        self.highlight_color = config.get_color('text_highlight')
        self.background_color = config.get_color('background')
        
        # Animation
        self.animation_timer = 0
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, text, x, y, width, height, color, hover_color, is_hovered=False):
        """Draw a button"""
        button_color = hover_color if is_hovered else color
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        # Draw text
        self.draw_text(text, self.font_medium, (255, 255, 255), x + width//2, y + height//2)
        return button_rect
    
    def update_animation(self):
        """Update animation timer"""
        self.animation_timer += 1
    
    def handle_event(self, event):
        """Handle menu events - to be implemented by subclass"""
        return None
    
    def draw(self):
        """Draw menu - to be implemented by subclass"""
        pass