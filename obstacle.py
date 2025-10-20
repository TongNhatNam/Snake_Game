"""
Obstacle system for Snake Game
Creates various types of obstacles that the snake must avoid
"""

import pygame
import random
import math
from config import config

class Obstacle:
    """Base obstacle class"""
    
    def __init__(self, x, y, obstacle_type="wall"):
        self.block_size = config.get_block_size()
        self.screen_width, self.screen_height = config.get_screen_size()
        self.obstacle_type = obstacle_type
        
        # Position and size
        self.x = x
        self.y = y
        self.width = self.block_size
        self.height = self.block_size
        
        # Visual effects
        self.animation_timer = 0
        self.pulse_scale = 1.0
        
        # Create rectangle for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        """Update obstacle animation"""
        self.animation_timer += 1
        self.pulse_scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.05)
    
    def draw(self, surface):
        """Draw the obstacle"""
        # Calculate animated size
        animated_width = self.width * self.pulse_scale
        animated_height = self.height * self.pulse_scale
        animated_x = self.x - (animated_width - self.width) / 2
        animated_y = self.y - (animated_height - self.height) / 2
        
        # Get color based on obstacle type
        color = self._get_color()
        
        # Draw main obstacle
        rect = pygame.Rect(animated_x, animated_y, animated_width, animated_height)
        pygame.draw.rect(surface, color, rect)
        
        # Draw border for better visibility
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        
        # Draw pattern based on type
        self._draw_pattern(surface, rect)
    
    def _get_color(self):
        """Get color based on obstacle type"""
        color_map = {
            "wall": config.get_color('obstacle'),
            "spike": (200, 50, 50),
            "ice": (100, 150, 255),
            "fire": (255, 100, 0)
        }
        return color_map.get(self.obstacle_type, config.get_color('obstacle'))
    
    def _draw_pattern(self, surface, rect):
        """Draw pattern based on obstacle type"""
        center_x, center_y = rect.center
        
        if self.obstacle_type == "spike":
            # Draw spikes
            points = [
                (center_x, center_y - 6),
                (center_x - 4, center_y + 2),
                (center_x + 4, center_y + 2)
            ]
            pygame.draw.polygon(surface, (255, 255, 255), points)
        
        elif self.obstacle_type == "ice":
            # Draw ice crystals
            for i in range(4):
                angle = i * 90 + self.animation_timer
                x = center_x + 3 * math.cos(math.radians(angle))
                y = center_y + 3 * math.sin(math.radians(angle))
                pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), 1)
        
        elif self.obstacle_type == "fire":
            # Draw fire effect
            for i in range(3):
                flame_x = center_x + (i - 1) * 2
                flame_y = center_y - 2 + i
                pygame.draw.circle(surface, (255, 255, 0), (flame_x, flame_y), 2)
    
    def get_rect(self):
        """Get obstacle rectangle for collision detection"""
        return self.rect

class ObstacleManager:
    """Manages obstacle generation and placement"""
    
    def __init__(self, game_area_x=0, game_area_y=0, game_area_width=800, game_area_height=600):
        self.obstacles = []
        self.obstacle_types = ["wall", "spike", "ice", "fire"]
        self.game_area_x = game_area_x
        self.game_area_y = game_area_y
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height
    
    def generate_level_obstacles(self, level, snake_body=None):
        """Generate obstacles for a specific level"""
        self.clear()
        
        # Get obstacle count for this level
        level_obstacles = config.get("levels.obstacle_count")
        obstacle_count = level_obstacles[min(level - 1, len(level_obstacles) - 1)]
        
        if obstacle_count == 0:
            return
        
        # Generate obstacles
        max_attempts = 200
        attempts = 0
        
        print(f"Generating {obstacle_count} obstacles for level {level}")
        
        while len(self.obstacles) < obstacle_count and attempts < max_attempts:
            attempts += 1
            
            # Random position within game area, aligned to grid
            grid_x = random.randrange(0, (self.game_area_width // config.get_block_size()))
            grid_y = random.randrange(0, (self.game_area_height // config.get_block_size()))
            x = self.game_area_x + grid_x * config.get_block_size()
            y = self.game_area_y + grid_y * config.get_block_size()
            
            # Random type
            obstacle_type = random.choice(self.obstacle_types)
            
            # Check if position is valid (not on snake, not overlapping other obstacles)
            if self._is_valid_position(x, y, snake_body):
                obstacle = Obstacle(x, y, obstacle_type)
                self.obstacles.append(obstacle)
                print(f"Created obstacle at ({x}, {y}) type: {obstacle_type}")
        
        print(f"Total obstacles created: {len(self.obstacles)}")
    
    def _is_valid_position(self, x, y, snake_body=None):
        """Check if position is valid for obstacle placement"""
        if snake_body is None:
            snake_body = []
        
        # Check collision with snake
        for block in snake_body:
            if x == block[0] and y == block[1]:
                return False
        
        # Check collision with existing obstacles
        new_rect = pygame.Rect(x, y, config.get_block_size(), config.get_block_size())
        for obstacle in self.obstacles:
            if new_rect.colliderect(obstacle.get_rect()):
                return False
        
        return True
    
    def update(self):
        """Update all obstacles"""
        for obstacle in self.obstacles:
            obstacle.update()
    
    def draw(self, surface):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            obstacle.draw(surface)
    
    def check_collision(self, rect):
        """Check collision with any obstacle"""
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle.get_rect()):
                return True
        return False
    
    def clear(self):
        """Clear all obstacles"""
        self.obstacles.clear()
    
    def get_obstacle_count(self):
        """Get current number of obstacles"""
        return len(self.obstacles)

class MovingObstacle(Obstacle):
    """Moving obstacle that follows a pattern"""
    
    def __init__(self, x, y, obstacle_type="wall", move_pattern="horizontal", speed=1):
        super().__init__(x, y, obstacle_type)
        self.move_pattern = move_pattern
        self.speed = speed
        self.original_x = x
        self.original_y = y
        self.move_timer = 0
        self.direction = 1
    
    def update(self):
        """Update obstacle position and animation"""
        super().update()
        self.move_timer += 1
        
        # Move based on pattern
        if self.move_pattern == "horizontal":
            self.x += self.speed * self.direction
            if self.x <= 0 or self.x >= self.screen_width - self.width:
                self.direction *= -1
        elif self.move_pattern == "vertical":
            self.y += self.speed * self.direction
            if self.y <= 0 or self.y >= self.screen_height - self.height:
                self.direction *= -1
        elif self.move_pattern == "circular":
            angle = self.move_timer * 0.02
            radius = 50
            self.x = self.original_x + radius * math.cos(angle)
            self.y = self.original_y + radius * math.sin(angle)
        
        # Update rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
