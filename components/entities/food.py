"""
Food system for Snake Game
Includes different types of food with various effects
"""

import pygame
import random
import math
from ..core import config

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
        
        # Lifetime system (only for special/bad food)
        if food_type == "special":
            self.lifetime = config.get("food.special_lifetime")
            self.warning_time = config.get("food.special_warning_time")
        elif food_type == "bad":
            self.lifetime = config.get("food.bad_lifetime")
            self.warning_time = config.get("food.bad_warning_time")
        else:
            self.lifetime = None  # Normal food doesn't expire
            self.warning_time = 0
        
        self.age = 0
        self.is_warning = False
        self.alpha = 255
        
        # Initialize position
        if x is None or y is None:
            self.randomize_position()
    
    def randomize_position(self, snake_body=None, obstacles=None):
        """Generate random position avoiding snake and obstacles"""
        if snake_body is None:
            snake_body = []
        if obstacles is None:
            obstacles = []
        
        MAX_ATTEMPTS = 50  # Constant for better maintainability
        max_attempts = MAX_ATTEMPTS
        for _ in range(max_attempts):
            self.x = round(random.randrange(self.game_area_x, self.game_area_x + self.game_area_width - self.block_size) / self.block_size) * self.block_size
            self.y = round(random.randrange(self.game_area_y, self.game_area_y + self.game_area_height - self.block_size) / self.block_size) * self.block_size
            
            food_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
            
            # Check all collisions in one pass
            collision = any([
                any(self.x == block[0] and self.y == block[1] for block in snake_body),
                any(food_rect.colliderect(obstacle.rect) for obstacle in obstacles)
            ])
            
            if not collision:
                break
    
    def update(self, delta_time=16):
        """Update food animation and lifetime"""
        try:
            # Update age for special/bad food
            if self.lifetime is not None:
                self.age += delta_time
                remaining_time = self.lifetime - self.age
                
                if remaining_time <= 0:
                    return False  # Food should be removed
                elif remaining_time <= self.warning_time:
                    self.is_warning = True
                    # Fade effect in warning phase
                    fade_progress = max(0, remaining_time / self.warning_time)
                    self.alpha = int(128 + 127 * fade_progress)  # 128-255 alpha
                else:
                    self.is_warning = False
                    self.alpha = 255
            
            # Update animations - optimized
            self.animation_timer += 1
            
            if self.is_warning:
                # Warning animation - faster pulse
                self.pulse_scale = 1.0 + 0.4 * math.sin(self.animation_timer * 0.2)
            else:
                # Normal animation
                self.pulse_scale = 1.0 + 0.2 * math.sin(self.animation_timer * 0.1)
            
            self.rotation += 2
            return True  # Food is still alive
        except Exception:
            return False
    
    def draw(self, surface):
        """Draw the food with optimized rendering"""
        # Calculate animated position and size
        pulse_offset = (self.block_size * (self.pulse_scale - 1.0)) / 2
        animated_x = int(self.x - pulse_offset)
        animated_y = int(self.y - pulse_offset)
        animated_size = int(self.block_size * self.pulse_scale)
        
        # Get color based on food type
        color = self._get_color()
        
        # Modify color for warning state
        if self.is_warning and int(self.animation_timer / 8) % 2:
            if self.food_type == "special":
                color = (255, 200, 100)  # Orange warning
            elif self.food_type == "bad":
                color = (255, 100, 100)  # Red warning
        
        # Optimized drawing
        rect = pygame.Rect(animated_x, animated_y, animated_size, animated_size)
        
        # Optimized alpha rendering
        if self.alpha < 255:
            # Use color with alpha instead of creating surface
            alpha_color = (*color, self.alpha)
            # Create temporary surface only when necessary
            temp_surface = pygame.Surface((animated_size, animated_size), pygame.SRCALPHA)
            temp_surface.fill(alpha_color)
            surface.blit(temp_surface, rect.topleft)
        else:
            # Direct drawing for full opacity
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
        self.game_area_x = game_area_x
        self.game_area_y = game_area_y
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height
        
        # Separate tracking for different food types
        self.normal_foods = []  # Always maintain 1 normal food
        self.special_foods = []  # Timer-based special foods
        self.bad_foods = []     # Timer-based bad foods
        
        # Timers for special foods
        self.special_spawn_timer = 0
        self.special_spawn_interval = self._get_random_interval("special")
        self.bad_spawn_timer = 0
        self.bad_spawn_interval = self._get_random_interval("bad")
    
    def _get_random_interval(self, food_type):
        """Get random spawn interval for special/bad food"""
        if food_type == "special":
            min_interval = config.get("food.special_spawn_interval_min")
            max_interval = config.get("food.special_spawn_interval_max")
        else:  # bad
            min_interval = config.get("food.bad_spawn_interval_min")
            max_interval = config.get("food.bad_spawn_interval_max")
        return random.randint(min_interval, max_interval)
    
    def spawn_food(self, snake_body=None, obstacles=None, food_type="normal"):
        """Spawn a specific type of food"""
        try:
            food = Food(food_type=food_type)
            food.game_area_x = self.game_area_x
            food.game_area_y = self.game_area_y
            food.game_area_width = self.game_area_width
            food.game_area_height = self.game_area_height
            food.randomize_position(snake_body, obstacles)
            
            # Add to appropriate list
            if food_type == "normal":
                self.normal_foods.append(food)
            elif food_type == "special":
                self.special_foods.append(food)
            elif food_type == "bad":
                self.bad_foods.append(food)
            
            # Update main foods list
            self._update_foods_list()
        except Exception:
            pass
    
    def ensure_normal_food(self, snake_body=None, obstacles=None):
        """Ensure there's always 1 normal food on screen"""
        if len(self.normal_foods) == 0:
            self.spawn_food(snake_body, obstacles, "normal")
    
    def update(self, delta_time=16):
        """Update all food items and spawn timers"""
        # Update existing foods and remove expired ones
        self.normal_foods = [food for food in self.normal_foods if food.update(delta_time)]
        self.special_foods = [food for food in self.special_foods if food.update(delta_time)]
        self.bad_foods = [food for food in self.bad_foods if food.update(delta_time)]
        
        # Update main foods list
        self.foods = self.normal_foods + self.special_foods + self.bad_foods
        
        # Update spawn timers
        self.special_spawn_timer += delta_time
        self.bad_spawn_timer += delta_time
        
        # Spawn special food if timer reached and none exists
        if (len(self.special_foods) == 0 and 
            self.special_spawn_timer >= self.special_spawn_interval):
            self.spawn_food(food_type="special")
            self.special_spawn_timer = 0
            self.special_spawn_interval = self._get_random_interval("special")
        
        # Spawn bad food if timer reached and none exists
        if (len(self.bad_foods) == 0 and 
            self.bad_spawn_timer >= self.bad_spawn_interval):
            self.spawn_food(food_type="bad")
            self.bad_spawn_timer = 0
            self.bad_spawn_interval = self._get_random_interval("bad")
    
    def draw(self, surface):
        """Draw all food items"""
        for food in self.foods:
            food.draw(surface)
    
    def check_collision(self, snake_head_rect):
        """Check collision with snake head and return collided food"""
        try:
            # Check all food types in order of priority
            food_lists = [
                (self.normal_foods, 'normal'),
                (self.special_foods, 'special'), 
                (self.bad_foods, 'bad')
            ]
            
            for food_list, food_type in food_lists:
                for i, food in enumerate(food_list):
                    if snake_head_rect.colliderect(food.get_rect()):
                        removed_food = food_list.pop(i)
                        self._update_foods_list()
                        return removed_food
            
            return None
        except Exception:
            return None
    
    def _update_foods_list(self):
        """Update main foods list after changes"""
        self.foods = self.normal_foods + self.special_foods + self.bad_foods
    
    def clear(self):
        """Clear all foods"""
        try:
            self.foods.clear()
            self.normal_foods.clear()
            self.special_foods.clear()
            self.bad_foods.clear()
            self.special_spawn_timer = 0
            self.bad_spawn_timer = 0
            self.special_spawn_interval = self._get_random_interval("special")
            self.bad_spawn_interval = self._get_random_interval("bad")
        except Exception:
            # Fallback to default intervals if config access fails
            self.special_spawn_interval = 20000  # 20 seconds default
            self.bad_spawn_interval = 30000     # 30 seconds default
    
    def get_food_count(self):
        """Get current number of foods on screen"""
        return len(self.foods)
