"""
Game-specific menu classes
"""

import pygame
from .base_menu import Menu
from ..core import config

class MainMenu(Menu):
    """Main menu screen"""
    
    def __init__(self, screen):
        super().__init__(screen)
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "High Scores", "Quit"]
        self.buttons = []

    def handle_event(self, event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                selected_action = self.options[self.selected_option]
                if selected_action == "Start Game":
                    return "Select Level"
                return selected_action
        return None

    def draw(self):
        """Draw main menu"""
        self.screen.fill(self.background_color)

        # Title with animation
        title_y = 150 + 10 * pygame.math.Vector2(0, 1).rotate(self.animation_timer * 2).y
        self.draw_text("SNAKE GAME", self.font_large, self.highlight_color,
                      self.screen_width // 2, title_y)

        # Subtitle
        self.draw_text("Enhanced Edition", self.font_medium, self.text_color,
                      self.screen_width // 2, title_y + 60)

        # Menu options
        start_y = 300
        button_width = 300
        button_height = 50
        button_spacing = 70

        self.buttons = []
        for i, option in enumerate(self.options):
            y = start_y + i * button_spacing
            is_selected = (i == self.selected_option)

            button_rect = self.draw_button(
                option,
                self.screen_width // 2 - button_width // 2,
                y,
                button_width,
                button_height,
                (50, 50, 50) if not is_selected else (100, 100, 100),
                (150, 150, 150),
                is_selected
            )
            self.buttons.append(button_rect)

        # Instructions
        self.draw_text("Use ARROW KEYS to navigate, ENTER to select",
                      self.font_small, self.text_color,
                      self.screen_width // 2, self.screen_height - 50)

        self.update_animation()

class LevelSelectMenu(Menu):
    """Level selection menu screen"""

    def __init__(self, screen):
        super().__init__(screen)
        self.selected_level = 0
        self.max_level = config.get("levels.max_level")
        self.level_names = config.get("levels.level_names")
        self.obstacle_counts = config.get("levels.obstacle_count")
        self.speed_multipliers = config.get("levels.speed_multiplier")

    def handle_event(self, event):
        """Handle level selection events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % self.max_level
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % self.max_level
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return f"start_level_{self.selected_level + 1}"
            elif event.key == pygame.K_ESCAPE:
                return "back"
        return None

    def draw(self):
        """Draw level selection menu"""
        self.screen.fill(self.background_color)

        # Title
        self.draw_text("SELECT DIFFICULTY", self.font_large, self.highlight_color,
                      self.screen_width // 2, 100)

        # Level options
        start_y = 200
        level_height = 80

        for i in range(self.max_level):
            y = start_y + i * level_height
            is_selected = (i == self.selected_level)

            # Level name
            level_name = self.level_names[i] if i < len(self.level_names) else f"Level {i + 1}"
            color = self.highlight_color if is_selected else self.text_color

            # Draw level box
            box_width = 400
            box_height = 60
            box_x = self.screen_width // 2 - box_width // 2
            box_y = y - 10

            # Box background
            box_color = (100, 100, 100) if is_selected else (50, 50, 50)
            pygame.draw.rect(self.screen, box_color, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

            # Level name
            self.draw_text(level_name, self.font_medium, color,
                          self.screen_width // 2, y)

            # Level details
            obstacle_count = self.obstacle_counts[i] if i < len(self.obstacle_counts) else 0
            speed_mult = self.speed_multipliers[i] if i < len(self.speed_multipliers) else 1.0

            details_text = f"Obstacles: {obstacle_count} | Speed: {speed_mult:.1f}x"
            self.draw_text(details_text, self.font_small, color,
                          self.screen_width // 2, y + 25)

        # Instructions
        self.draw_text("Use ARROW KEYS to select, ENTER to start",
                      self.font_small, self.text_color,
                      self.screen_width // 2, self.screen_height - 100)
        self.draw_text("Press ESC to go back",
                      self.font_small, self.text_color,
                      self.screen_width // 2, self.screen_height - 50)

        self.update_animation()

class GameOverMenu(Menu):
    """Game over screen"""

    def __init__(self, screen, final_score, level):
        super().__init__(screen)
        self.final_score = final_score
        self.level = level
        from .score_menu import HighScoreMenu
        self.high_score_menu = HighScoreMenu(screen)
        self.show_high_score = False

        # Add score to high scores
        self.high_score_menu.add_score(final_score, level)

    def handle_event(self, event):
        """Handle game over events"""
        if self.show_high_score:
            result = self.high_score_menu.handle_event(event)
            if result == "back":
                self.show_high_score = False
            return result

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "restart"
            elif event.key == pygame.K_m:
                return "menu"
            elif event.key == pygame.K_h:
                self.show_high_score = True
            elif event.key == pygame.K_q:
                return "quit"
        return None

    def draw(self):
        """Draw game over screen"""
        if self.show_high_score:
            self.high_score_menu.draw()
            return

        self.screen.fill(self.background_color)

        # Game Over text with animation
        game_over_y = 150 + 5 * pygame.math.Vector2(0, 1).rotate(self.animation_timer * 3).y
        self.draw_text("GAME OVER", self.font_large, (255, 0, 0),
                      self.screen_width // 2, game_over_y)

        # Final score
        self.draw_text(f"Final Score: {self.final_score:06d}", self.font_medium, self.highlight_color,
                      self.screen_width // 2, 250)

        # Level reached
        self.draw_text(f"Level Reached: {self.level}", self.font_medium, self.text_color,
                      self.screen_width // 2, 300)

        # Options
        options = [
            ("R - Play Again", (0, 255, 0)),
            ("M - Main Menu", (255, 255, 0)),
            ("H - High Scores", (0, 255, 255)),
            ("Q - Quit", (255, 0, 0))
        ]

        start_y = 400
        for i, (text, color) in enumerate(options):
            y = start_y + i * 40
            self.draw_text(text, self.font_medium, color, self.screen_width // 2, y)

        self.update_animation()