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
        
        # Particles for effects
        self.particles = []
    
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
        """Draw modern button with smooth effects"""
        button_rect = pygame.Rect(x, y, width, height)
        
        # Smooth transition between states
        button_color = hover_color if is_hovered else color
        
        # Create gradient fill for button - more refined
        for i in range(height):
            progress = i / height
            if is_hovered:
                # Brighter gradient when hovered
                line_color = tuple(
                    int(button_color[j] + (255 - button_color[j]) * progress * 0.2)
                    for j in range(3)
                )
            else:
                # Subtle darkening
                line_color = tuple(
                    int(button_color[j] * (0.85 + progress * 0.15))
                    for j in range(3)
                )
            pygame.draw.line(self.screen, line_color, (x, y + i), (x + width, y + i))
        
        # Draw shadow/glow effect
        if is_hovered:
            # Glow effect with blurred appearance
            for offset in [8, 6, 4]:
                glow_color = (255, 200, 100)
                alpha_val = int(30 * (1 - offset / 8))
                glow_rect = pygame.Rect(x - offset//2, y - offset//2, width + offset, height + offset)
                glow_surface = pygame.Surface((width + offset, height + offset))
                glow_surface.set_alpha(alpha_val)
                glow_surface.fill(glow_color)
                self.screen.blit(glow_surface, (x - offset//2, y - offset//2))
        
        # Border with better styling
        border_thickness = 2
        border_color = (100, 150, 255) if is_hovered else (150, 150, 200)
        
        # Draw rounded corners effect with lines
        corner_radius = 8
        # Top border
        pygame.draw.line(self.screen, border_color, (x + corner_radius, y), (x + width - corner_radius, y), border_thickness)
        # Bottom border
        pygame.draw.line(self.screen, border_color, (x + corner_radius, y + height), (x + width - corner_radius, y + height), border_thickness)
        # Left border
        pygame.draw.line(self.screen, border_color, (x, y + corner_radius), (x, y + height - corner_radius), border_thickness)
        # Right border
        pygame.draw.line(self.screen, border_color, (x + width, y + corner_radius), (x + width, y + height - corner_radius), border_thickness)
        
        # Text with elegant shadow
        text_color = (255, 255, 255) if is_hovered else (220, 220, 230)
        
        # Soft shadow
        self.draw_text(text, self.font_medium, (0, 0, 0), 
                      x + width//2 + 1, y + height//2 + 1, shadow=False)
        self.draw_text(text, self.font_medium, text_color, 
                      x + width//2, y + height//2, shadow=False)
        
        return button_rect
    
    def draw_gradient_background(self, color1=(20, 30, 60), color2=(40, 60, 120)):
        """Draw gradient background"""
        for y in range(self.screen_height):
            # Linear interpolation between color1 and color2
            progress = y / self.screen_height
            color = tuple(int(color1[i] + (color2[i] - color1[i]) * progress) for i in range(3))
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))
    
    def draw_animated_particles(self):
        """Draw and update animated particles"""
        for particle in self.particles[:]:
            # Update particle
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vy'] += 0.1  # Gravity
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Draw particle with fade
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = particle['color']
            size = max(1, int(particle['size'] * (particle['life'] / particle['max_life'])))
            
            try:
                pygame.draw.circle(self.screen, color, 
                                 (int(particle['x']), int(particle['y'])), size)
            except ValueError:
                pass
    
    def spawn_particles(self, x, y, count=5, color=(100, 200, 255)):
        """Spawn animated particles"""
        import random
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed - 1,
                'life': 30,
                'max_life': 30,
                'color': color,
                'size': random.randint(3, 6)
            })
    
    def update_animation(self):
        """Update animation timer"""
        self.animation_timer += 1
    
    def handle_event(self, event):
        """Handle menu events - to be implemented by subclass"""
        return None
    
    def draw(self):
        """Draw menu - to be implemented by subclass"""
        pass