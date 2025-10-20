"""
Food system for Snake Game
Includes different types of food with various effects
"""

import pygame
import random
import math
from config import config

class Food:
    """Base food class"""
    
    def __init__(self, x=None, y=None, food_type="normal"):
        self.block_size = config.get_block_size()
        self.food_type = food_type
        # Game area bounds (will be set by FoodManager)
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
        
        # Initialize position
        if x is None or y is None:
            self.randomize_position()
    
    def randomize_position(self, snake_body=None, obstacles=None):
        """Generate random position avoiding snake and obstacles"""
        if snake_body is None:
            snake_body = []
        if obstacles is None:
            obstacles = []
        
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
                food_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
                for obstacle in obstacles:
                    if food_rect.colliderect(obstacle.rect):
                        collision = True
                        break
            
            if not collision:
                break
    
    def update(self):
        """Update food animation"""
        self.animation_timer += 1
        self.pulse_scale = 1.0 + 0.2 * math.sin(self.animation_timer * 0.1)
        self.rotation += 2
    
    def draw(self, surface):
        """Draw the food with animation effects"""
        # Calculate animated position and size
        pulse_offset = (self.block_size * (self.pulse_scale - 1.0)) / 2
        animated_x = self.x - pulse_offset
        animated_y = self.y - pulse_offset
        animated_size = self.block_size * self.pulse_scale
        
        # Get color based on food type
        color = self._get_color()
        
        # Draw main food
        rect = pygame.Rect(animated_x, animated_y, animated_size, animated_size)
        pygame.draw.rect(surface, color, rect)
        
        # Add special effects based on type
        self._draw_special_effects(surface, rect)
    
    def _get_color(self):
        """Get color based on food type"""
        color_map = {
            "normal": config.get_color('food_normal'),
            "special": config.get_color('food_special'),
            "bad": config.get_color('food_bad')
        }
        return color_map.get(self.food_type, config.get_color('food_normal'))
    
    def _draw_special_effects(self, surface, rect):
        """Draw special visual effects"""
        if self.food_type == "special":
            # Golden glow effect
            glow_rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
            pygame.draw.rect(surface, (255, 255, 0), glow_rect, 2)
            
            # Sparkle effect
            center_x = rect.centerx
            center_y = rect.centery
            for i in range(4):
                angle = self.rotation + i * 90
                sparkle_x = center_x + math.cos(math.radians(angle)) * 15
                sparkle_y = center_y + math.sin(math.radians(angle)) * 15
                pygame.draw.circle(surface, (255, 255, 255), (int(sparkle_x), int(sparkle_y)), 2)
        
        elif self.food_type == "bad":
            # Warning effect
            warning_rect = pygame.Rect(rect.x - 3, rect.y - 3, rect.width + 6, rect.height + 6)
            pygame.draw.rect(surface, (255, 0, 0), warning_rect, 2)
            
            # Skull symbol
            center_x, center_y = rect.center
            pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y - 2), 3)
            pygame.draw.circle(surface, (0, 0, 0), (center_x - 2, center_y + 2), 2)
            pygame.draw.circle(surface, (0, 0, 0), (center_x + 2, center_y + 2), 2)
    
    def get_score(self):
        """Get score value for this food"""
        score_map = {
            "normal": config.get("food.normal_score"),
            "special": config.get("food.special_score"),
            "bad": -config.get("food.bad_penalty")
        }
        return score_map.get(self.food_type, 0)
    
    def get_rect(self):
        """Get food rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.block_size, self.block_size)
    
    def get_type(self):
        """Get food type"""
        return self.food_type

class FoodManager:
    """Manages multiple food items and their spawning"""
    
    def __init__(self, game_area_x=0, game_area_y=0, game_area_width=800, game_area_height=600):
        self.foods = []
        self.special_spawn_chance = config.get("food.special_spawn_chance")
        self.bad_spawn_chance = 0.05  # 5% chance for bad food
        self.max_foods = 3  # Maximum number of foods on screen
        self.game_area_x = game_area_x
        self.game_area_y = game_area_y
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height
    
    def spawn_food(self, snake_body=None, obstacles=None):
        """Spawn a new food item"""
        if len(self.foods) >= self.max_foods:
            return
        
        # Determine food type
        rand = random.random()
        if rand < self.special_spawn_chance:
            food_type = "special"
        elif rand < self.special_spawn_chance + self.bad_spawn_chance:
            food_type = "bad"
        else:
            food_type = "normal"
        
        food = Food(food_type=food_type)
        food.game_area_x = self.game_area_x
        food.game_area_y = self.game_area_y
        food.game_area_width = self.game_area_width
        food.game_area_height = self.game_area_height
        food.randomize_position(snake_body, obstacles)
        self.foods.append(food)
    
    def update(self):
        """Update all food items"""
        for food in self.foods:
            food.update()
    
    def draw(self, surface):
        """Draw all food items"""
        for food in self.foods:
            food.draw(surface)
    
    def check_collision(self, snake_head_rect):
        """Check collision with snake head and return collided food"""
        for i, food in enumerate(self.foods):
            if snake_head_rect.colliderect(food.get_rect()):
                return self.foods.pop(i)
        return None
    
    def clear(self):
        """Clear all foods"""
        self.foods.clear()
    
    def get_food_count(self):
        """Get current number of foods on screen"""
        return len(self.foods)
