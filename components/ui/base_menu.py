"""
Base Menu class for all menu screens
"""

import pygame
import math
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
    
    def draw_text(self, text, font, color, x, y, center=True, shadow=False):
        """Draw text with optional shadow effect"""
        if shadow:
            # Draw shadow
            shadow_surface = font.render(text, True, (0, 0, 0))
            if center:
                shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
            else:
                shadow_rect = shadow_surface.get_rect(topleft=(x + 2, y + 2))
            self.screen.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, text, x, y, width, height, color, hover_color, is_hovered=False):
        """Draw an enhanced button with gradient effect"""
        button_color = hover_color if is_hovered else color
        button_rect = pygame.Rect(x, y, width, height)
        
        # Draw button with gradient effect
        if is_hovered:
            # Brighter gradient for hover
            for i in range(height):
                shade = int(button_color[0] * (1 - i / height * 0.3))
                line_color = (shade, shade, shade)
                pygame.draw.line(self.screen, line_color, (x, y + i), (x + width, y + i))
        else:
            pygame.draw.rect(self.screen, button_color, button_rect)
        
        # Border with glow effect for selected
        border_color = (255, 255, 100) if is_hovered else (255, 255, 255)
        border_width = 3 if is_hovered else 2
        pygame.draw.rect(self.screen, border_color, button_rect, border_width)
        
        # Draw text with shadow
        text_color = (255, 255, 255)
        self.draw_text(text, self.font_medium, text_color, x + width//2, y + height//2, shadow=True)
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