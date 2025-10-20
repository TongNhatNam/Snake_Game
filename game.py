"""
Main game file for Enhanced Snake Game
Integrates all game components and manages the game loop
"""

import pygame
import sys
import time
import random
from config import config
from snake import Snake
from food import FoodManager
from powerup import PowerUpManager
from obstacle import ObstacleManager
from menu import MainMenu, LevelSelectMenu, SettingsMenu, HighScoreMenu, GameOverMenu

class SnakeGame:
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        
        # Get configuration
        self.screen_width, self.screen_height = config.get_screen_size()
        self.fps = config.get_fps()
        self.block_size = config.get_block_size()
        
        # Create screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Enhanced Snake Game")
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = "menu"  # menu, playing, paused, game_over
        self.level = 1
        self.score = 0
        self.high_score = 0
        
        # Game objects
        self.snake = None
        self.food_manager = None
        self.powerup_manager = None
        self.obstacle_manager = None
        
        # Menus
        self.main_menu = MainMenu(self.screen)
        self.level_select_menu = LevelSelectMenu(self.screen)
        self.settings_menu = SettingsMenu(self.screen)
        self.high_score_menu = HighScoreMenu(self.screen)
        self.game_over_menu = None
        
        # Game settings
        self.current_fps = self.fps
        
        # Snake movement timer (independent of FPS)
        self.snake_move_timer = 0
        self.snake_move_interval = 200  # Move every 200ms (5 times per second)
        
        # Countdown
        self.countdown_timer = 0
        self.countdown_duration = 3000  # 3 seconds
        
        # Pause
        self.pause_timer = 0
        
        # Game area boundaries
        self.game_area_width = 400
        self.game_area_height = 400
        self.game_area_x = 50
        self.game_area_y = 50
        
        # Fonts
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
    
    def start_new_game(self, selected_level=1):
        """Start a new game with selected level"""
        self.state = "countdown"
        self.level = selected_level
        self.score = 0
        self.countdown_timer = 0
        
        # Create game objects with game area bounds
        self.snake = Snake(self.game_area_x + self.game_area_width//2, self.game_area_y + self.game_area_height//2, 
                          self.game_area_x, self.game_area_y, self.game_area_width, self.game_area_height)
        self.food_manager = FoodManager(self.game_area_x, self.game_area_y, self.game_area_width, self.game_area_height)
        self.powerup_manager = PowerUpManager(self.game_area_x, self.game_area_y, self.game_area_width, self.game_area_height)
        self.obstacle_manager = ObstacleManager(self.game_area_x, self.game_area_y, self.game_area_width, self.game_area_height)
        
        # Generate level obstacles
        self.obstacle_manager.generate_level_obstacles(self.level, self.snake.body)
        
        # Spawn initial food
        self.food_manager.spawn_food(self.snake.body, self.obstacle_manager.obstacles)
        
        # Update base FPS from config (in case it was changed in settings)
        self.fps = config.get_fps()
        self.current_fps = self.fps  # FPS only affects smoothness, not snake speed
        
        # Set snake movement speed based on level
        level_speed_multiplier = config.get("levels.speed_multiplier")
        if self.level <= len(level_speed_multiplier):
            # Faster levels = shorter move interval
            base_interval = 200  # 200ms base interval
            speed_multiplier = level_speed_multiplier[self.level - 1]
            self.snake_move_interval = int(base_interval / speed_multiplier)
        else:
            self.snake_move_interval = 200
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle events based on current state
            if self.state == "menu":
                result = self.main_menu.handle_event(event)
                if result == "Start Game":
                    self.start_new_game(1)  # Start with level 1
                elif result == "Select Level":
                    self.state = "level_select"
                elif result == "Settings":
                    self.state = "settings"
                elif result == "High Scores":
                    self.state = "high_scores"
                elif result == "Quit":
                    return False
            
            elif self.state == "level_select":
                result = self.level_select_menu.handle_event(event)
                if result and result.startswith("start_level_"):
                    level = int(result.split("_")[2])
                    self.start_new_game(level)
                elif result == "back":
                    self.state = "menu"
            
            elif self.state == "settings":
                result = self.settings_menu.handle_event(event)
                if result == "back":
                    self.state = "menu"
                    # Update screen size if changed
                    new_width, new_height = config.get_screen_size()
                    if new_width != self.screen_width or new_height != self.screen_height:
                        self.screen_width, self.screen_height = new_width, new_height
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                        self.main_menu = MainMenu(self.screen)
                        self.settings_menu = SettingsMenu(self.screen)
                        self.high_score_menu = HighScoreMenu(self.screen)
                    
                    # Update FPS if changed
                    new_fps = config.get_fps()
                    if new_fps != self.fps:
                        self.fps = new_fps
                        # Update current FPS if not in game
                        if self.state == "menu":
                            self.current_fps = self.fps
            
            elif self.state == "high_scores":
                result = self.high_score_menu.handle_event(event)
                if result == "back":
                    self.state = "menu"
            
            elif self.state == "countdown":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
            
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                    elif event.key == pygame.K_SPACE:
                        self.state = "paused"
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(-self.block_size, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(self.block_size, 0)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(0, -self.block_size)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(0, self.block_size)
            
            elif self.state == "paused":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
            
            elif self.state == "game_over":
                result = self.game_over_menu.handle_event(event)
                if result == "restart":
                    self.start_new_game(self.level)
                elif result == "menu":
                    self.state = "menu"
                elif result == "quit":
                    return False
        
        return True
    
    def update_game(self):
        """Update game logic"""
        if self.state != "playing":
            return
        
        # Update power-up timers every frame (independent of movement)
        delta_time = self.clock.get_time()
        self.snake._update_power_ups(delta_time)
        
        # Update snake movement timer
        self.snake_move_timer += delta_time
        
        # Check if it's time to move snake
        move_interval = self.snake_move_interval
        
        # Adjust movement speed based on power-ups
        active_powerups = self.snake.get_power_ups()
        if 'slow_motion' in active_powerups:
            move_interval *= 2  # Move half as often
        # Note: speed_boost was removed, so no speed increase
        
        if self.snake_move_timer >= move_interval:
            self.snake.move()
            self.snake_move_timer = 0
        
        # Check collisions
        if self.snake.check_collision():
            if self.snake.lose_life():
                self.game_over()
                return
            else:
                # Reset snake position but keep playing
                pass
        
        # Check obstacle collision
        if self.snake.check_obstacle_collision(self.obstacle_manager.obstacles):
            if self.snake.lose_life():
                self.game_over()
                return
        
        # Check food collision
        food = self.food_manager.check_collision(self.snake.get_head_rect())
        if food:
            score_change = food.get_score()
            self.score += score_change
            
            if score_change > 0:
                self.snake.grow()
            else:
                self.snake.shrink()
            
            # Spawn new food
            self.food_manager.spawn_food(self.snake.body, self.obstacle_manager.obstacles)
        
        # Check power-up collision
        powerup = self.powerup_manager.check_collision(self.snake.get_head_rect())
        if powerup:
            powerup_type = powerup.get_type()
            duration = powerup.get_duration()
            print(f"Power-up collected: {powerup_type}, duration: {duration}ms")
            self.snake.apply_power_up(powerup_type, duration)
        
        # Update managers
        self.food_manager.update()
        self.powerup_manager.update()
        self.obstacle_manager.update()
        
        # Spawn power-ups periodically
        if len(self.powerup_manager.powerups) == 0:
            self.powerup_manager.spawn_powerup(self.snake.body, self.obstacle_manager.obstacles, self.food_manager.foods)
        
    
    def game_over(self):
        """Handle game over"""
        self.state = "game_over"
        self.game_over_menu = GameOverMenu(self.screen, self.score, self.level)
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
    
    def draw_countdown(self):
        """Draw countdown screen"""
        self.screen.fill(config.get_color('background'))
        
        # Countdown text
        remaining_time = self.countdown_duration - self.countdown_timer
        if remaining_time > 2000:
            count_text = "3"
        elif remaining_time > 1000:
            count_text = "2"
        else:
            count_text = "1"
        
        # Animate countdown
        scale = 1.0 + 0.5 * (1.0 - (remaining_time % 1000) / 1000.0)
        font_size = int(100 * scale)
        font = pygame.font.Font(None, font_size)
        
        text_surface = font.render(count_text, True, config.get_color('text_highlight'))
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Instructions
        self.draw_text("Get Ready!", self.font_medium, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 100)
        self.draw_text("Press ESC to cancel", self.font_small, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 150)
    
    def draw_pause(self):
        """Draw pause screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(config.get_color('background'))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        self.draw_text("PAUSED", self.font_large, config.get_color('text_highlight'),
                      self.screen_width // 2, self.screen_height // 2 - 50)
        self.draw_text("Press SPACE to continue", self.font_medium, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 20)
        self.draw_text("Press ESC for main menu", self.font_medium, config.get_color('text'),
                      self.screen_width // 2, self.screen_height // 2 + 60)
    
    def draw_hud(self):
        """Draw heads-up display"""
        # Sidebar area (right side of game area)
        sidebar_x = self.game_area_x + self.game_area_width + 20
        
        # Score
        self.draw_text(f"Score: {self.score:06d}", self.font_medium, config.get_color('text'),
                      sidebar_x, 80, False)
        
        # Level
        self.draw_text(f"Level: {self.level}", self.font_medium, config.get_color('text'),
                      sidebar_x, 120, False)
        
        # Lives
        lives_text = "♥" * self.snake.get_lives()
        self.draw_text(f"Lives: {lives_text}", self.font_medium, config.get_color('text'),
                      sidebar_x, 160, False)
        
        # Speed (movement interval)
        speed_text = f"Speed: {int(1000/self.snake_move_interval):.1f}/sec"
        self.draw_text(speed_text, self.font_small, config.get_color('text'),
                      sidebar_x, 200, False)
        
        # Power-ups
        active_powerups = self.snake.get_power_ups()
        if active_powerups:
            powerup_timers = self.snake.get_power_up_timers()
            self.draw_text("Power-ups:", self.font_small, config.get_color('text_highlight'),
                          sidebar_x, 240, False)
            y_offset = 260
            for k, v in powerup_timers.items():
                self.draw_text(f"{k}: {int(v/1000)}s", self.font_small, config.get_color('text'),
                              sidebar_x, y_offset, False)
                y_offset += 20
        
        # Instructions at bottom
        self.draw_text("Controls:", self.font_small, config.get_color('text_highlight'),
                      sidebar_x, 350, False)
        self.draw_text("WASD/Arrows: Move", self.font_small, config.get_color('text'),
                      sidebar_x, 370, False)
        self.draw_text("SPACE: Pause", self.font_small, config.get_color('text'),
                      sidebar_x, 390, False)
        self.draw_text("ESC: Menu", self.font_small, config.get_color('text'),
                      sidebar_x, 410, False)
    
    def draw_game(self):
        """Draw game elements"""
        # Clear screen
        self.screen.fill(config.get_color('background'))
        
        # Draw game area border
        game_rect = pygame.Rect(self.game_area_x-2, self.game_area_y-2, self.game_area_width+4, self.game_area_height+4)
        pygame.draw.rect(self.screen, (255, 255, 255), game_rect, 2)
        
        # Fill game area background
        game_bg = pygame.Rect(self.game_area_x, self.game_area_y, self.game_area_width, self.game_area_height)
        pygame.draw.rect(self.screen, (20, 20, 20), game_bg)
        
        # Draw game objects
        self.obstacle_manager.draw(self.screen)
        self.food_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.snake.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game
            if self.state == "playing":
                self.update_game()
            elif self.state == "countdown":
                self.countdown_timer += self.clock.get_time()
                if self.countdown_timer >= self.countdown_duration:
                    self.state = "playing"
            
            # Draw
            if self.state == "menu":
                self.main_menu.draw()
            elif self.state == "level_select":
                self.level_select_menu.draw()
            elif self.state == "settings":
                self.settings_menu.draw()
            elif self.state == "high_scores":
                self.high_score_menu.draw()
            elif self.state == "countdown":
                self.draw_countdown()
            elif self.state == "playing":
                self.draw_game()
            elif self.state == "paused":
                self.draw_game()
                self.draw_pause()
            elif self.state == "game_over":
                self.game_over_menu.draw()
            
            # Update display
            pygame.display.flip()
            
            # Control FPS
            if self.state == "playing":
                self.clock.tick(self.current_fps)
            else:
                self.clock.tick(60)
        
        # Cleanup
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
