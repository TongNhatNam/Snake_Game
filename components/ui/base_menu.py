"""
Base Menu class for all menu screens
"""

import pygame
import math
from ..core import config

class Menu:
    """Base menu class with performance optimizations"""
    
    # Class-level font cache
    _font_cache = {}
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = 1000, 700  # Fixed optimal size
        
        # Cached fonts for performance
        self.font_large = self._get_cached_font(60)
        self.font_medium = self._get_cached_font(40)
        self.font_small = self._get_cached_font(30)
        
        # Cached colors
        self.text_color = config.get_color('text')
        self.highlight_color = config.get_color('text_highlight')
        self.background_color = config.get_color('background')
        
        # Animation
        self.animation_timer = 0
        
        # Text surface cache for frequently used text
        self._text_cache = {}
    
    @classmethod
    def _get_cached_font(cls, size):
        """Get cached font for performance"""
        if size not in cls._font_cache:
            try:
                cls._font_cache[size] = pygame.font.Font(None, size)
            except pygame.error:
                cls._font_cache[size] = pygame.font.Font(pygame.font.get_default_font(), size)
        return cls._font_cache[size]
    
    def draw_text(self, text, font, color, x, y, center=True, shadow=False):
        """Draw text with optimized caching and optional shadow"""
        # Create cache key with limited cache size
        cache_key = (str(text), id(font), color, shadow)
        
        if cache_key not in self._text_cache:
            # Limit cache size to prevent memory issues
            if len(self._text_cache) > 100:
                # Remove oldest entries (simple FIFO)
                oldest_keys = list(self._text_cache.keys())[:20]
                for key in oldest_keys:
                    del self._text_cache[key]
            
            if shadow:
                shadow_surface = font.render(str(text), True, (0, 0, 0))
                text_surface = font.render(str(text), True, color)
                self._text_cache[cache_key] = (shadow_surface, text_surface)
            else:
                text_surface = font.render(str(text), True, color)
                self._text_cache[cache_key] = (None, text_surface)
        
        shadow_surface, text_surface = self._text_cache[cache_key]
        
        if shadow and shadow_surface:
            if center:
                shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
            else:
                shadow_rect = shadow_surface.get_rect(topleft=(x + 2, y + 2))
            self.screen.blit(shadow_surface, shadow_rect)
        
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, text, x, y, width, height, color, hover_color, is_hovered=False):
        """Draw optimized button"""
        button_rect = pygame.Rect(x, y, width, height)
        button_color = hover_color if is_hovered else color
        
        # Simple rect for performance
        pygame.draw.rect(self.screen, button_color, button_rect)
        
        # Border
        border_color = (255, 255, 100) if is_hovered else (200, 200, 200)
        pygame.draw.rect(self.screen, border_color, button_rect, 2)
        
        # Text
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