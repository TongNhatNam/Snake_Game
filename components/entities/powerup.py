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

        # Game area
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
        
        # Lifetime system
        self.lifetime = config.get("powerups.lifetime")
        self.warning_time = config.get("powerups.warning_time")
        self.fade_time = config.get("powerups.fade_time")
        self.age = 0
        self.is_warning = False
        self.is_fading = False
        self.alpha = 255
        
        # Duration when picked up
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
        
        MAX_ATTEMPTS = 50  # Constant for better maintainability
        max_attempts = MAX_ATTEMPTS
        for _ in range(max_attempts):
            self.x = round(random.randrange(self.game_area_x, self.game_area_x + self.game_area_width - self.block_size) / self.block_size) * self.block_size
            self.y = round(random.randrange(self.game_area_y, self.game_area_y + self.game_area_height - self.block_size) / self.block_size) * self.block_size
            
            powerup_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
            
            # Check all collisions in one pass
            collision = any([
                any(self.x == block[0] and self.y == block[1] for block in snake_body),
                any(powerup_rect.colliderect(obstacle.rect) for obstacle in obstacles),
                any(powerup_rect.colliderect(food.get_rect()) for food in foods)
            ])
            
            if not collision:
                break
    
    def update(self, delta_time=16):
        """Update power-up animation and lifetime"""
        # Update age
        self.age += delta_time
        
        # Check lifetime phases
        remaining_time = self.lifetime - self.age
        
        if remaining_time <= 0:
            return False  # Power-up should be removed
        elif remaining_time <= self.fade_time:
            self.is_fading = True
            self.is_warning = True
            # Fade out effect
            fade_progress = remaining_time / self.fade_time
            self.alpha = int(255 * fade_progress)
        elif remaining_time <= self.warning_time:
            self.is_warning = True
            self.is_fading = False
            self.alpha = 255
        else:
            self.is_warning = False
            self.is_fading = False
            self.alpha = 255
        
        # Update animations
        self.animation_timer += 1
        
        if self.is_warning:
            # Warning animation - faster pulse and blink
            self.pulse_scale = 1.0 + 0.5 * math.sin(self.animation_timer * 0.3)
            self.glow_intensity = 0.8 + 0.2 * math.sin(self.animation_timer * 0.4)
        else:
            # Normal animation
            self.pulse_scale = 1.0 + 0.3 * math.sin(self.animation_timer * 0.15)
            self.glow_intensity = 0.5 + 0.5 * math.sin(self.animation_timer * 0.2)
        
        self.rotation += 3
        return True  # Power-up is still alive
    
    def draw(self, surface):
        """Draw the power-up with optimized rendering"""
        # Calculate animated position and size
        pulse_offset = (self.block_size * (self.pulse_scale - 1.0)) / 2
        animated_x = int(self.x - pulse_offset)
        animated_y = int(self.y - pulse_offset)
        animated_size = int(self.block_size * self.pulse_scale)
        
        # Get color based on power-up type and state
        color = self._get_color()
        
        # Modify color for warning/fading states
        if self.is_fading:
            fade_progress = 1.0 - (self.alpha / 255.0)
            color = (
                min(255, color[0] + int(100 * fade_progress)),
                max(0, color[1] - int(100 * fade_progress)),
                max(0, color[2] - int(100 * fade_progress))
            )
        elif self.is_warning and int(self.animation_timer / 10) % 2:
            color = (255, 100, 100)
        
        # Optimized drawing - single surface approach
        total_size = animated_size + 16
        powerup_surface = pygame.Surface((total_size, total_size), pygame.SRCALPHA)
        
        # Draw glow effect - optimized
        if self.glow_intensity > 0.1:  # Skip minimal glow for performance
            glow_alpha = int(min(self.alpha, 100 * self.glow_intensity))
            if glow_alpha > 10:  # Only draw visible glow
                glow_rect = pygame.Rect(4, 4, animated_size + 8, animated_size + 8)
                # Draw glow directly without extra surface
                glow_color = (*color, glow_alpha)
                pygame.draw.rect(powerup_surface, color, glow_rect)
                powerup_surface.set_alpha(glow_alpha)
                powerup_surface.set_alpha(255)  # Reset alpha
        
        # Draw main power-up with border
        main_rect = pygame.Rect(8, 8, animated_size, animated_size)
        pygame.draw.rect(powerup_surface, color, main_rect)
        pygame.draw.rect(powerup_surface, (255, 255, 255), main_rect, 2)
        
        # Draw symbol
        self._draw_symbol(powerup_surface, main_rect)
        
        # Apply alpha and blit
        if self.alpha < 255:
            powerup_surface.set_alpha(self.alpha)
        
        surface.blit(powerup_surface, (animated_x - 8, animated_y - 8))
    
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
        self.next_spawn_interval = self._get_random_spawn_interval()
        self.cooldown_timer = 0
        self.game_area_x = game_area_x
        self.game_area_y = game_area_y
        self.game_area_width = game_area_width
        self.game_area_height = game_area_height
    
    def _get_random_spawn_interval(self):
        """Get random spawn interval between min and max"""
        min_interval = config.get("powerups.spawn_interval_min")
        max_interval = config.get("powerups.spawn_interval_max")
        return random.randint(min_interval, max_interval)
    
    def update(self, delta_time=16):
        """Update all power-ups and spawn timer"""
        # Update existing power-ups and remove expired ones
        self.powerups = [powerup for powerup in self.powerups if powerup.update(delta_time)]
        
        # Update cooldown timer
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time
        
        # Update spawn timer
        self.spawn_timer += delta_time
        
        # Remove excessive debug logging for better performance
        
        # Spawn new power-up if conditions are met
        if (len(self.powerups) < self.max_powerups and 
            self.spawn_timer >= self.next_spawn_interval and 
            self.cooldown_timer <= 0 and
            random.random() < self.spawn_chance):
            # PowerUp spawned successfully
            self.spawn_powerup()
            self.spawn_timer = 0
            self.next_spawn_interval = self._get_random_spawn_interval()
    
    def spawn_powerup(self, snake_body=None, obstacles=None, foods=None):
        """Spawn a random power-up"""
        if len(self.powerups) >= self.max_powerups:
            return
        
        try:
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
        except Exception:
            pass
    
    def draw(self, surface):
        """Draw all power-ups"""
        for powerup in self.powerups:
            powerup.draw(surface)
    
    def check_collision(self, snake_head_rect):
        """Check collision with snake head and return collided power-up"""
        for i, powerup in enumerate(self.powerups):
            if snake_head_rect.colliderect(powerup.get_rect()):
                # Start cooldown after pickup
                self.cooldown_timer = config.get("powerups.cooldown_after_pickup")
                return self.powerups.pop(i)
        return None
    
    def clear(self):
        """Clear all power-ups"""
        self.powerups.clear()
        self.spawn_timer = 0
        self.cooldown_timer = 0
        self.next_spawn_interval = self._get_random_spawn_interval()
    
    def get_powerup_count(self):
        """Get current number of power-ups on screen"""
        return len(self.powerups)
