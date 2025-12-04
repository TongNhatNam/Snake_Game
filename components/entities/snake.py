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
        

    
    def grow(self, amount=1):
        """Grow the snake by specified amount"""
        self.length += amount
    
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
        """Draw the snake with modern design"""
        try:
            snake_color = config.get_color('snake')
            head_color = config.get_color('snake_head')
            
            for i, block in enumerate(self.body):
                is_head = (i == len(self.body) - 1)
                color = head_color if is_head else snake_color
                
                if is_head and any(self.power_ups.values()):
                    color = tuple(min(255, c + 50) for c in color)
                
                x, y = int(block[0]), int(block[1])
                
                if is_head:
                    self._draw_head(surface, x, y, color)
                else:
                    self._draw_body_segment(surface, x, y, color, i == len(self.body) - 2)
        except (pygame.error, AttributeError, ValueError, TypeError):
            pass
    
    def _draw_head(self, surface, x, y, color):
        """Draw snake head with eyes and modern design"""
        try:
            # Main head
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            
            # Draw head base
            pygame.draw.rect(surface, color, rect)
            
            # Head border
            lighter_color = tuple(min(255, c + 40) for c in color)
            pygame.draw.rect(surface, lighter_color, rect, 2)
            
            # Draw eyes based on direction
            eye_color = (0, 0, 0)  # Black eyes
            eye_outline = (255, 255, 255)  # White outline
            eye_size = 3
            
            center_x = x + self.block_size // 2
            center_y = y + self.block_size // 2
            
            if self.x_change > 0:  # Moving right
                left_eye = (center_x + 4, center_y - 3)
                right_eye = (center_x + 4, center_y + 3)
            elif self.x_change < 0:  # Moving left
                left_eye = (center_x - 4, center_y - 3)
                right_eye = (center_x - 4, center_y + 3)
            elif self.y_change > 0:  # Moving down
                left_eye = (center_x - 3, center_y + 4)
                right_eye = (center_x + 3, center_y + 4)
            else:  # Moving up (default)
                left_eye = (center_x - 3, center_y - 4)
                right_eye = (center_x + 3, center_y - 4)
            
            pygame.draw.circle(surface, eye_color, left_eye, eye_size)
            pygame.draw.circle(surface, eye_color, right_eye, eye_size)
            pygame.draw.circle(surface, eye_outline, left_eye, eye_size, 1)
            pygame.draw.circle(surface, eye_outline, right_eye, eye_size, 1)
            
        except Exception:
            pass
    
    def _draw_body_segment(self, surface, x, y, color, is_neck=False):
        """Draw body segment with gradient effect"""
        try:
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            
            # Main body
            segment_color = color if not is_neck else tuple(min(255, c + 20) for c in color)
            pygame.draw.rect(surface, segment_color, rect)
            
            # Border
            border_color = tuple(min(255, c + 30) for c in color)
            pygame.draw.rect(surface, border_color, rect, 1)
            
            if is_neck:
                highlight_color = tuple(min(255, c + 50) for c in color)
                pygame.draw.line(surface, highlight_color, 
                               (x + 2, y + 2), (x + self.block_size - 2, y + 2), 1)
        except Exception:
            pass
    
    def check_collision(self):
        """Check for collisions with walls and self"""
        try:
            # Wall collision
            if not self.power_ups['wall_pass']:
                if (self.x >= self.game_area_x + self.game_area_width or self.x < self.game_area_x or 
                    self.y >= self.game_area_y + self.game_area_height or self.y < self.game_area_y):
                    return True
            
            # Wall pass
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
            
            # Self collision
            if len(self.body) > 1:
                head_pos = [self.x, self.y]
                return head_pos in self.body[:-1]
            return False
        except (IndexError, TypeError, KeyError):
            return True 
    
    def check_obstacle_collision(self, obstacles):
        """Check collision with obstacles"""
        try:
            if self.power_ups.get('wall_pass'):
                return False
            head_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
            return any(head_rect.colliderect(obstacle.rect) for obstacle in obstacles)
        except (AttributeError, TypeError):
            return False
    
    def change_direction(self, dx, dy):
        """Change snake direction with improved logic"""
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
