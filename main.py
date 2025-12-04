import pygame
import sys
import asyncio
from components.core import config, GameState, EventHandler, GameRenderer, achievement_manager
from components.entities import Snake, FoodManager, PowerUpManager, ObstacleManager
from components.ui import MainMenu, LevelSelectMenu, SettingsMenu, HighScoreMenu, GameOverMenu, AchievementMenu, AchievementNotification

class SnakeGame:
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        try:
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
            
            # Fonts for notifications
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 30)
            
            # Death notification
            self.death_notification_time = 0
            self.death_notification_duration = 0
            self.lives_remaining = 0
            

        except Exception:
            sys.exit(1)
    
    def _init_menus(self):
        """Initialize all menu objects"""
        try:
            self.menus = {
                "main": MainMenu(self.screen),
                "level_select": LevelSelectMenu(self.screen),
                "settings": SettingsMenu(self.screen),
                "high_scores": HighScoreMenu(self.screen),
                "achievements": AchievementMenu(self.screen),
                "game_over": None
            }
            
            # Achievement notification system
            self.current_notification = None
        except Exception:
            raise
    
    def start_new_game(self, level=1):
        """Start a new game with selected level"""
        self.game_state.set_state("countdown")
        self.game_state.reset_for_new_game(level)
        
        # Track game start for achievements
        achievement_manager.update_stats("game_start")
        achievement_manager.reset_session_achievements()  # Reset session achievements for new game
        
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
        
        # Track game start time for survival achievements
        self.game_state.start_time = pygame.time.get_ticks()
    
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
        elif result == "Achievements":
            self.game_state.set_state("achievements")

        elif result == False:
            return False
        
        return True
    

    
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
            achievement_manager.update_stats("death")
            if snake.lose_life():
                self._game_over()
                return
            else:
                # Still have lives left - show retry message
                self._show_death_notification(snake.get_lives())
        
        # Obstacle collision
        if snake.check_obstacle_collision(self.game_objects["obstacle_manager"].obstacles):
            achievement_manager.update_stats("death")
            if snake.lose_life():
                self._game_over()
                return
            else:
                # Still have lives left - show retry message
                self._show_death_notification(snake.get_lives())
        
        # Food collision
        food = self.game_objects["food_manager"].check_collision(snake.get_head_rect())
        if food:
            score_change = food.get_score()
            self.game_state.score += score_change
            
            # No eat sound
            
            # Track food eaten for achievements
            food_type = "normal" if score_change == 10 else "special" if score_change > 0 else "bad"
            achievement_manager.update_stats("food_eaten", food_type=food_type)
            
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
            
            # No powerup sound
            
            # Track power-up collection for achievements
            achievement_manager.update_stats("powerup_collected")
    
    def _update_managers(self):
        """Update all managers"""
        delta_time = self.clock.get_time()
        self.game_objects["food_manager"].update(delta_time)
        self.game_objects["powerup_manager"].update(delta_time)
        self.game_objects["obstacle_manager"].update()
    
    def _game_over(self):
        """Handle game over"""
        
        # Track game end for achievements
        achievement_manager.update_stats("game_end")
        achievement_manager.check_achievements()
        
        self.game_state.set_state("game_over")
        self.menus["game_over"] = GameOverMenu(
            self.screen, self.game_state.score, self.game_state.level
        )
    
    def _show_death_notification(self, lives_remaining):
        """Show notification when snake dies but still has lives"""
        # Create temporary notification
        self.death_notification_time = pygame.time.get_ticks()
        self.death_notification_duration = 2000  # 2 seconds
        self.lives_remaining = lives_remaining
    
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
        elif state == "achievements":
            self.menus["achievements"].draw()
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
        """Main game loop - wrapper for async version"""
        asyncio.run(self.async_run())
    
    async def async_run(self):
        """Main game loop - async version for web"""
        running = True
        
        try:
            while running:
                # Handle events
                running = self._handle_events()
                
                # Update achievements
                self._update_achievements()
                
                # Update countdown
                if self.game_state.state == "countdown":
                    self.game_state.countdown_timer += self.clock.get_time()
                    if self.game_state.countdown_timer >= self.game_state.countdown_duration:
                        self.game_state.set_state("playing")
                
                # Update game
                self._update_game()
                
                # Draw
                self._draw()
                
                # Draw achievement notification
                self._draw_achievement_notification()
                
                pygame.display.flip()
                
                # Control FPS
                fps = 60 if self.game_state.is_playing() else config.get_fps()
                self.clock.tick(fps)
                
                # Critical for web - yield to browser
                await asyncio.sleep(0)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            pass
        except (pygame.error, SystemExit) as e:
            # Handle pygame and system exit errors
            pass
        except (MemoryError, OSError) as e:
            # Handle system resource errors
            pass
        finally:
            # Cleanup
            try:
                achievement_manager.save_progress()
            except Exception:
                pass
            pygame.quit()
            sys.exit()
    
    def _update_achievements(self):
        """Update achievement system (optimized)"""
        delta_time = self.clock.get_time()
        
        # Update survival time only when playing
        if self.game_state.is_playing():
            survival_time = (pygame.time.get_ticks() - getattr(self.game_state, 'start_time', 0)) / 1000
            achievement_manager.update_stats("survival_time", time=survival_time)
            
            # Update score and level (less frequent updates)
            achievement_manager.update_stats("score_update", score=self.game_state.score)
            achievement_manager.update_stats("level_update", level=self.game_state.level)
            
            # Check achievements only when playing
            achievement_manager.check_achievements()
        
        # Update notification timer
        achievement_manager.update_notification_timer(delta_time)
        
        # Handle notifications
        if not self.current_notification:
            notification_achievement = achievement_manager.get_notification()
            if notification_achievement:
                self.current_notification = AchievementNotification(notification_achievement)
        
        # Update current notification
        if self.current_notification:
            if not self.current_notification.update(delta_time):
                self.current_notification = None
    
    def _draw_achievement_notification(self):
        """Draw achievement notification overlay"""
        # Draw death notification (chết nhưng còn lượt) - at bottom
        if self.death_notification_time > 0:
            elapsed = pygame.time.get_ticks() - self.death_notification_time
            if elapsed < self.death_notification_duration:
                # Death message at bottom
                death_text = self.font_small.render(f"Lost 1 Life! {self.lives_remaining} Remaining", True, (255, 100, 100))
                death_rect = death_text.get_rect(center=(self.screen_width // 2, self.screen_height - 70))
                self.screen.blit(death_text, death_rect)
                
                # Retry message at very bottom
                retry_text = self.font_small.render("Use Arrow or WASD to play again", True, (200, 200, 200))
                retry_rect = retry_text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
                self.screen.blit(retry_text, retry_rect)
            else:
                self.death_notification_time = 0
        
        # Draw achievement notification
        if self.current_notification:
            self.current_notification.draw(self.screen, self.font_medium, self.font_small)

def main():
    """Main function"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()