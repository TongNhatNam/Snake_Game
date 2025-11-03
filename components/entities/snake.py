"""
Snake class for the Snake Game
Handles snake movement, growth, collision detection, and power-up effects
"""

import pygame
import random
from ..core import config

class Snake:
    """Snake class with enhanced features"""
    
    def __init__(self, x=None, y=None, game_area_x=0, game_area_y=0, game_area_width=800, game_area_height=600):
        """Initialize snake with optional starting position"""
        self.block_size = config.get_block_size()
        self.game_area_x = game_area_x
        self.game_area_y = game_area_y
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height
        
        # Initial position
        self.x = x if x is not None else game_area_x + game_area_width // 2
        self.y = y if y is not None else game_area_y + game_area_height // 2
        
        # Movement
        self.x_change = 0
        self.y_change = 0
        
        # Body and properties
        self.body = []
        self.length = 1
        self.lives = 3  # New: lives system
        
        # Power-up effects
        self.power_ups = {
            'slow_motion': False,
            'wall_pass': False
        }
        self.power_up_timers = {
            'slow_motion': 0,
            'wall_pass': 0
        }
        
        # Visual effects
        self.grow_animation = 0
        self.death_animation = 0
    
    def move(self):
        """Move the snake"""
        
        # Only move if there's a direction set
        if self.x_change == 0 and self.y_change == 0:
            return
        
        # Update head position (move by block size)
        self.x += self.x_change
        self.y += self.y_change
        
        # Add new head position to body
        head = [self.x, self.y]
        self.body.append(head)
        
        # Remove tail if body is too long
        if len(self.body) > self.length:
            del self.body[0]
        
        # Update grow animation
        if self.grow_animation > 0:
            self.grow_animation -= 1
    
    def grow(self, amount=1):
        """Grow the snake by specified amount"""
        self.length += amount
        self.grow_animation = 10  # Animation duration
    
    def shrink(self, amount=1):
        """Shrink the snake by specified amount"""
        self.length = max(1, self.length - amount)
        # Remove excess body parts
        while len(self.body) > self.length:
            del self.body[0]
    
    def lose_life(self):
        """Lose a life and reset position"""
        self.lives -= 1
        if self.lives > 0:
            self._reset_position()
        return self.lives <= 0
    
    def _reset_position(self):
        """Reset snake to center position"""
        self.x = self.game_area_x + self.game_area_width // 2
        self.y = self.game_area_y + self.game_area_height // 2
        self.x_change = 0
        self.y_change = 0
        self.body = []
        self.length = 1
        self.grow_animation = 0
        self.death_animation = 0
    
    def apply_power_up(self, power_up_type, duration):
        """Apply a power-up effect"""
        self.power_ups[power_up_type] = True
        self.power_up_timers[power_up_type] = duration
    
    def _update_power_ups(self, delta_time=16):
        """Update power-up timers and effects"""
        for power_up in list(self.power_ups.keys()):
            if self.power_ups[power_up] and self.power_up_timers[power_up] > 0:
                self.power_up_timers[power_up] -= delta_time
                if self.power_up_timers[power_up] <= 0:
                    self.power_ups[power_up] = False
    
    def draw(self, surface):
        """Draw the snake with enhanced visuals"""
        try:
            for i, block in enumerate(self.body):
                # Determine color based on position and effects
                if i == len(self.body) - 1:  # Head
                    color = config.get_color('snake_head')
                    # Add glow effect for power-ups
                    if any(self.power_ups.values()):
                        color = tuple(min(255, c + 50) for c in color)
                else:
                    color = config.get_color('snake')
                
                # Draw main body
                rect = pygame.Rect(block[0], block[1], self.block_size, self.block_size)
                pygame.draw.rect(surface, color, rect)
                
                # Add border for better visibility
                pygame.draw.rect(surface, (0, 0, 0), rect, 1)
                
                # Grow animation effect - optimized
                if i == len(self.body) - 1 and self.grow_animation > 0:
                    alpha = int(255 * (self.grow_animation / 10))
                    glow_surface = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
                    glow_surface.set_alpha(alpha)
                    glow_surface.fill(color)
                    surface.blit(glow_surface, (block[0], block[1]))
        except Exception:
            pass
    
    def check_collision(self):
        """Check for collisions with walls and self"""
        try:
            # Wall collision (with wall pass power-up check)
            if not self.power_ups['wall_pass']:
                if (self.x >= self.game_area_x + self.game_area_width or self.x < self.game_area_x or 
                    self.y >= self.game_area_y + self.game_area_height or self.y < self.game_area_y):
                    return True
            
            # Wall pass - wrap around game area
            if self.power_ups['wall_pass']:
                if self.x >= self.game_area_x + self.game_area_width:
                    self.x = self.game_area_x
                    if self.body:
                        self.body[-1][0] = self.x
                elif self.x < self.game_area_x:
                    self.x = self.game_area_x + self.game_area_width - self.block_size
                    if self.body:
                        self.body[-1][0] = self.x
                if self.y >= self.game_area_y + self.game_area_height:
                    self.y = self.game_area_y
                    if self.body:
                        self.body[-1][1] = self.y
                elif self.y < self.game_area_y:
                    self.y = self.game_area_y + self.game_area_height - self.block_size
                    if self.body:
                        self.body[-1][1] = self.y
            
            # Self collision - optimized check
            if len(self.body) > 1:
                head_pos = [self.x, self.y]
                return head_pos in self.body[:-1]
            
            return False
        except (IndexError, TypeError, KeyError):
            return True  # Treat errors as collision
    
    def check_obstacle_collision(self, obstacles):
        """Check collision with obstacles"""
        try:
            # Wall pass does NOT protect against obstacles
            head_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
            return any(head_rect.colliderect(obstacle.rect) for obstacle in obstacles)
        except (AttributeError, TypeError):
            return False
    
    def change_direction(self, dx, dy):
        """Change snake direction with improved logic"""
        # Prevent 180-degree turns
        if dx != 0 and self.x_change != -dx:
            self.x_change = dx
            self.y_change = 0
        elif dy != 0 and self.y_change != -dy:
            self.x_change = 0
            self.y_change = dy
    
    def get_head_rect(self):
        """Get rectangle for snake head (useful for collision detection)"""
        return pygame.Rect(self.x, self.y, self.block_size, self.block_size)
    
    def is_alive(self):
        """Check if snake is still alive"""
        return self.lives > 0
    
    def get_lives(self):
        """Get current number of lives"""
        return self.lives
    
    def get_length(self):
        """Get current snake length"""
        return self.length
    
    def get_power_ups(self):
        """Get active power-ups"""
        return {k: v for k, v in self.power_ups.items() if v}
    
    def get_power_up_timers(self):
        """Get remaining time for power-ups"""
        return {k: v for k, v in self.power_up_timers.items() if self.power_ups[k]}
