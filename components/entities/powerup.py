"""
Power-up system for Snake Game
Includes various power-ups with different effects
"""

import pygame
import random
import math
from ..core import config

class PowerUp:
    """Base power-up class"""
    
    def __init__(self, x=None, y=None, power_type="speed_boost"):
        self.block_size = config.get_block_size()
        self.power_type = power_type
        # Game area bounds (will be set by PowerUpManager)
        self.game_area_x = 0
        self.game_area_y = 0
        self.game_area_width = 800
        self.game_area_height = 600
        
        # Position
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0
        
        # Visual effects
        self.animation_timer = 0
        self.pulse_scale = 1.0
        self.rotation = 0
        self.glow_intensity = 0
        
        # Duration
        self.duration = self._get_duration()
        
        # Initialize position
        if x is None or y is None:
            self.randomize_position()
    
    def _get_duration(self):
        """Get duration based on power-up type"""
        duration_map = {
            "slow_motion": config.get("powerups.slow_duration"),
            "wall_pass": config.get("powerups.wall_duration")
        }
        return duration_map.get(self.power_type, 5000)
    
    def randomize_position(self, snake_body=None, obstacles=None, foods=None):
        """Generate random position avoiding snake, obstacles, and foods"""
        if snake_body is None:
            snake_body = []
        if obstacles is None:
            obstacles = []
        if foods is None:
            foods = []
        
        max_attempts = 100
        for _ in range(max_attempts):
            self.x = round(random.randrange(self.game_area_x, self.game_area_x + self.game_area_width - self.block_size) / self.block_size) * self.block_size
            self.y = round(random.randrange(self.game_area_y, self.game_area_y + self.game_area_height - self.block_size) / self.block_size) * self.block_size
            
            # Check collision with snake
            collision = False
            for block in snake_body:
                if self.x == block[0] and self.y == block[1]:
                    collision = True
                    break
            
            # Check collision with obstacles
            if not collision:
                powerup_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
                for obstacle in obstacles:
                    if powerup_rect.colliderect(obstacle.rect):
                        collision = True
                        break
            
            # Check collision with foods
            if not collision:
                for food in foods:
                    if powerup_rect.colliderect(food.get_rect()):
                        collision = True
                        break
            
            if not collision:
                break
    
    def update(self):
        """Update power-up animation"""
        self.animation_timer += 1
        self.pulse_scale = 1.0 + 0.3 * math.sin(self.animation_timer * 0.15)
        self.rotation += 3
        self.glow_intensity = 0.5 + 0.5 * math.sin(self.animation_timer * 0.2)
    
    def draw(self, surface):
        """Draw the power-up with special effects"""
        # Calculate animated position and size
        pulse_offset = (self.block_size * (self.pulse_scale - 1.0)) / 2
        animated_x = self.x - pulse_offset
        animated_y = self.y - pulse_offset
        animated_size = self.block_size * self.pulse_scale
        
        # Get color based on power-up type
        color = self._get_color()
        
        # Draw glow effect
        glow_size = animated_size + 8
        glow_x = animated_x - 4
        glow_y = animated_y - 4
        glow_alpha = int(100 * self.glow_intensity)
        
        glow_surface = pygame.Surface((glow_size, glow_size))
        glow_surface.set_alpha(glow_alpha)
        glow_surface.fill(color)
        surface.blit(glow_surface, (glow_x, glow_y))
        
        # Draw main power-up
        rect = pygame.Rect(animated_x, animated_y, animated_size, animated_size)
        pygame.draw.rect(surface, color, rect)
        
        # Draw border
        pygame.draw.rect(surface, (255, 255, 255), rect, 2)
        
        # Draw symbol
        self._draw_symbol(surface, rect)
    
    def _get_color(self):
        """Get color based on power-up type"""
        color_map = {
            "slow_motion": config.get_color('powerup_slow'),
            "wall_pass": config.get_color('powerup_wall')
        }
        return color_map.get(self.power_type, config.get_color('powerup_slow'))
    
    def _draw_symbol(self, surface, rect):
        """Draw symbol representing the power-up"""
        center_x, center_y = rect.center
        
        if self.power_type == "slow_motion":
            # Clock symbol
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), 6, 2)
            # Hour hand
            hour_x = center_x + 2 * math.cos(math.radians(self.rotation))
            hour_y = center_y + 2 * math.sin(math.radians(self.rotation))
            pygame.draw.line(surface, (255, 255, 255), (center_x, center_y), (hour_x, hour_y), 2)
            # Minute hand
            minute_x = center_x + 4 * math.cos(math.radians(self.rotation * 2))
            minute_y = center_y + 4 * math.sin(math.radians(self.rotation * 2))
            pygame.draw.line(surface, (255, 255, 255), (center_x, center_y), (minute_x, minute_y), 2)
        
        elif self.power_type == "wall_pass":
            # Wall with arrow symbol
            pygame.draw.rect(surface, (255, 255, 255), (center_x - 4, center_y - 2, 8, 4))
            # Arrow pointing through
            points = [(center_x + 2, center_y - 1), (center_x + 4, center_y), (center_x + 2, center_y + 1)]
            pygame.draw.polygon(surface, (255, 255, 255), points)
    
    def get_rect(self):
        """Get power-up rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.block_size, self.block_size)
    
    def get_type(self):
        """Get power-up type"""
        return self.power_type
    
    def get_duration(self):
        """Get power-up duration in milliseconds"""
        return self.duration

class PowerUpManager:
    """Manages power-up spawning and effects"""
    
    def __init__(self, game_area_x=0, game_area_y=0, game_area_width=800, game_area_height=600):
        self.powerups = []
        self.spawn_chance = config.get("powerups.spawn_chance")
        self.max_powerups = 1  # Maximum power-ups on screen
        self.spawn_timer = 0
        self.spawn_interval = 45000  # 45 seconds between spawns
        self.game_area_x = game_area_x
        self.game_area_y = game_area_y
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height
    
    def update(self):
        """Update all power-ups and spawn timer"""
        # Update existing power-ups
        for powerup in self.powerups:
            powerup.update()
        
        # Update spawn timer
        self.spawn_timer += 16  # Assuming 60 FPS
        
        # Spawn new power-up if conditions are met
        if (len(self.powerups) < self.max_powerups and 
            self.spawn_timer >= self.spawn_interval and 
            random.random() < self.spawn_chance):
            self.spawn_powerup()
            self.spawn_timer = 0
    
    def spawn_powerup(self, snake_body=None, obstacles=None, foods=None):
        """Spawn a random power-up"""
        if len(self.powerups) >= self.max_powerups:
            return
        
        # Random power-up type
        power_types = ["slow_motion", "wall_pass"]
        power_type = random.choice(power_types)
        
        powerup = PowerUp(power_type=power_type)
        powerup.game_area_x = self.game_area_x
        powerup.game_area_y = self.game_area_y
        powerup.game_area_width = self.game_area_width
        powerup.game_area_height = self.game_area_height
        powerup.randomize_position(snake_body, obstacles, foods)
        self.powerups.append(powerup)
    
    def draw(self, surface):
        """Draw all power-ups"""
        for powerup in self.powerups:
            powerup.draw(surface)
    
    def check_collision(self, snake_head_rect):
        """Check collision with snake head and return collided power-up"""
        for i, powerup in enumerate(self.powerups):
            if snake_head_rect.colliderect(powerup.get_rect()):
                return self.powerups.pop(i)
        return None
    
    def clear(self):
        """Clear all power-ups"""
        self.powerups.clear()
        self.spawn_timer = 0
    
    def get_powerup_count(self):
        """Get current number of power-ups on screen"""
        return len(self.powerups)
