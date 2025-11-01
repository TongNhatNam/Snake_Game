"""
Main game file for Enhanced Snake Game
Integrates all game components and manages the game loop
"""

import pygame
import sys
from components.core import config, GameState, EventHandler, GameRenderer
from components.entities import Snake, FoodManager, PowerUpManager, ObstacleManager
from components.ui import MainMenu, LevelSelectMenu, SettingsMenu, HighScoreMenu, GameOverMenu

class SnakeGame:
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        
        # Screen setup
        self.screen_width, self.screen_height = config.get_screen_size()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Enhanced Snake Game")
        self.clock = pygame.time.Clock()
        
        # Core components
        self.game_state = GameState()
        self.renderer = GameRenderer(self.screen)
        
        # Game objects
        self.game_objects = {}
        
        # Initialize menus
        self._init_menus()
        
        # Event handler
        self.event_handler = EventHandler(
            self.game_state, 
            self.menus, 
            config.get_block_size()
        )
    
    def _init_menus(self):
        """Initialize all menu objects"""
        self.menus = {
            "main": MainMenu(self.screen),
            "level_select": LevelSelectMenu(self.screen),
            "settings": SettingsMenu(self.screen),
            "high_scores": HighScoreMenu(self.screen),
            "game_over": None
        }
    
    def start_new_game(self, level=1):
        """Start a new game with selected level"""
        self.game_state.set_state("countdown")
        self.game_state.reset_for_new_game(level)
        
        # Create game objects
        area = self.game_state
        self.game_objects = {
            "snake": Snake(
                area.game_area_x + area.game_area_width//2, 
                area.game_area_y + area.game_area_height//2,
                area.game_area_x, area.game_area_y, 
                area.game_area_width, area.game_area_height
            ),
            "food_manager": FoodManager(
                area.game_area_x, area.game_area_y, 
                area.game_area_width, area.game_area_height
            ),
            "powerup_manager": PowerUpManager(
                area.game_area_x, area.game_area_y, 
                area.game_area_width, area.game_area_height
            ),
            "obstacle_manager": ObstacleManager(
                area.game_area_x, area.game_area_y, 
                area.game_area_width, area.game_area_height
            )
        }
        
        # Setup level
        self.game_objects["obstacle_manager"].generate_level_obstacles(
            level, self.game_objects["snake"].body
        )
        self.game_objects["food_manager"].spawn_food(
            self.game_objects["snake"].body, 
            self.game_objects["obstacle_manager"].obstacles,
            "normal"
        )
        
        # Set movement speed based on level
        self._set_movement_speed(level)
    
    def _set_movement_speed(self, level):
        """Set snake movement speed based on level"""
        speed_multipliers = config.get("levels.speed_multiplier")
        if level <= len(speed_multipliers):
            multiplier = speed_multipliers[level - 1]
            self.game_state.snake_move_interval = int(200 / multiplier)
    
    def _handle_events(self):
        """Handle all game events"""
        result = self.event_handler.handle_events(
            self.game_objects.get("snake")
        )
        
        if result == "start_game":
            self.start_new_game(1)
        elif isinstance(result, tuple) and result[0] == "start_level":
            self.start_new_game(result[1])
        elif result == "restart":
            self.start_new_game(self.game_state.level)
        elif result == "settings_changed":
            self._handle_settings_change()
        elif result == False:
            return False
        
        return True
    
    def _handle_settings_change(self):
        """Handle settings changes"""
        new_width, new_height = config.get_screen_size()
        if new_width != self.screen_width or new_height != self.screen_height:
            self.screen_width, self.screen_height = new_width, new_height
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self._init_menus()
            self.renderer = GameRenderer(self.screen)
    
    def _update_game(self):
        """Update game logic"""
        if not self.game_state.is_playing():
            return
        
        snake = self.game_objects["snake"]
        delta_time = self.clock.get_time()
        
        # Update power-ups
        snake._update_power_ups(delta_time)
        
        # Update movement timer
        self.game_state.snake_move_timer += delta_time
        
        # Move snake if it's time
        move_interval = self.game_state.snake_move_interval
        if 'slow_motion' in snake.get_power_ups():
            move_interval *= 2
        
        if self.game_state.snake_move_timer >= move_interval:
            snake.move()
            self.game_state.snake_move_timer = 0
        
        # Check collisions and update game
        self._check_collisions()
        self._update_managers()
    
    def _check_collisions(self):
        """Check all collision types"""
        snake = self.game_objects["snake"]
        
        # Wall/self collision
        if snake.check_collision():
            if snake.lose_life():
                self._game_over()
                return
        
        # Obstacle collision
        if snake.check_obstacle_collision(self.game_objects["obstacle_manager"].obstacles):
            if snake.lose_life():
                self._game_over()
                return
        
        # Food collision
        food = self.game_objects["food_manager"].check_collision(snake.get_head_rect())
        if food:
            score_change = food.get_score()
            self.game_state.score += score_change
            
            if score_change > 0:
                snake.grow()
            elif score_change < 0:
                snake.shrink()
            
            self.game_state.score = max(0, self.game_state.score)
            # Ensure normal food is always available
            self.game_objects["food_manager"].ensure_normal_food(
                snake.body, self.game_objects["obstacle_manager"].obstacles
            )
        
        # Power-up collision
        powerup = self.game_objects["powerup_manager"].check_collision(snake.get_head_rect())
        if powerup:
            snake.apply_power_up(powerup.get_type(), powerup.get_duration())
    
    def _update_managers(self):
        """Update all managers"""
        delta_time = self.clock.get_time()
        self.game_objects["food_manager"].update(delta_time)
        self.game_objects["powerup_manager"].update(delta_time)
        self.game_objects["obstacle_manager"].update()
    
    def _game_over(self):
        """Handle game over"""
        self.game_state.set_state("game_over")
        self.menus["game_over"] = GameOverMenu(
            self.screen, self.game_state.score, self.game_state.level
        )
    
    def _draw(self):
        """Draw everything based on current state"""
        state = self.game_state.state
        
        if state == "menu":
            self.menus["main"].draw()
        elif state == "level_select":
            self.menus["level_select"].draw()
        elif state == "settings":
            self.menus["settings"].draw()
        elif state == "high_scores":
            self.menus["high_scores"].draw()
        elif state == "countdown":
            self.renderer.draw_countdown(
                self.game_state.countdown_timer, 
                self.game_state.countdown_duration
            )
        elif state == "playing":
            self.renderer.draw_game(self.game_objects, self.game_state)
        elif state == "paused":
            self.renderer.draw_game(self.game_objects, self.game_state)
            self.renderer.draw_pause()
        elif state == "game_over":
            self.menus["game_over"].draw()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            running = self._handle_events()
            
            # Update countdown
            if self.game_state.state == "countdown":
                self.game_state.countdown_timer += self.clock.get_time()
                if self.game_state.countdown_timer >= self.game_state.countdown_duration:
                    self.game_state.set_state("playing")
            
            # Update game
            self._update_game()
            
            # Draw
            self._draw()
            pygame.display.flip()
            
            # Control FPS
            fps = 60 if self.game_state.is_playing() else config.get_fps()
            self.clock.tick(fps)
        
        # Cleanup
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()