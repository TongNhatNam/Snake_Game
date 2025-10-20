"""
Menu system for Snake Game
Handles main menu, settings, and game over screens
"""

import pygame
import json
import os
from config import config

class Menu:
    """Base menu class"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = config.get_screen_size()
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        
        # Colors
        self.text_color = config.get_color('text')
        self.highlight_color = config.get_color('text_highlight')
        self.background_color = config.get_color('background')
        
        # Animation
        self.animation_timer = 0
    
    def draw_text(self, text, font, color, x, y, center=True):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, text, x, y, width, height, color, hover_color, is_hovered=False):
        """Draw a button"""
        button_color = hover_color if is_hovered else color
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        # Draw text
        self.draw_text(text, self.font_medium, (255, 255, 255), x + width//2, y + height//2)
        return button_rect
    
    def update_animation(self):
        """Update animation timer"""
        self.animation_timer += 1

class MainMenu(Menu):
    """Main menu screen"""
    
    def __init__(self, screen):
        super().__init__(screen)
        self.selected_option = 0
        # --- THAY ĐỔI 1: Đã xóa "Select Level" khỏi danh sách này ---
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
                # --- THAY ĐỔI 2: Xử lý logic khi chọn "Start Game" ---
                selected_action = self.options[self.selected_option]

                if selected_action == "Start Game":
                    # Trả về "Select Level" để vòng lặp game chính biết
                    # cần chuyển sang màn hình LevelSelectMenu
                    return "Select Level"

                # Trả về các hành động khác như bình thường ("Settings", "High Scores", "Quit")
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

class SettingsMenu(Menu):
    """Settings menu screen"""

    def __init__(self, screen):
        super().__init__(screen)
        self.selected_setting = 0
        self.settings = [
            ("FPS", "screen.fps", [5, 10, 15, 20, 30, 60]),
            ("Screen Width", "screen.width", [600, 800, 1024, 1280]),
            ("Screen Height", "screen.height", [400, 600, 768, 720]),
            ("Snake Color", "colors.snake", [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]),
            ("Background Color", "colors.background", [(0, 0, 0), (20, 20, 20), (40, 40, 40), (60, 60, 60)])
        ]
        self.current_values = []
        self.load_current_values()

    def load_current_values(self):
        """Load current setting values"""
        self.current_values = []
        for setting_name, key_path, options in self.settings:
            current_value = config.get(key_path)
            if current_value in options:
                self.current_values.append(options.index(current_value))
            else:
                self.current_values.append(0)

    def handle_event(self, event):
        """Handle settings events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % len(self.settings)
            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % len(self.settings)
            elif event.key == pygame.K_LEFT:
                self.current_values[self.selected_setting] = max(0, self.current_values[self.selected_setting] - 1)
                self.update_setting()
            elif event.key == pygame.K_RIGHT:
                setting_name, key_path, options = self.settings[self.selected_setting]
                self.current_values[self.selected_setting] = min(len(options) - 1, self.current_values[self.selected_setting] + 1)
                self.update_setting()
            elif event.key == pygame.K_ESCAPE:
                return "back"
        return None

    def update_setting(self):
        """Update current setting value"""
        setting_name, key_path, options = self.settings[self.selected_setting]
        new_value = options[self.current_values[self.selected_setting]]
        config.set(key_path, new_value)
        config.save_config()

    def draw(self):
        """Draw settings menu"""
        self.screen.fill(self.background_color)

        # Title
        self.draw_text("SETTINGS", self.font_large, self.highlight_color,
                      self.screen_width // 2, 100)

        # Settings
        start_y = 200
        setting_height = 60

        for i, (setting_name, key_path, options) in enumerate(self.settings):
            y = start_y + i * setting_height
            is_selected = (i == self.selected_setting)

            # Setting name
            color = self.highlight_color if is_selected else self.text_color
            self.draw_text(setting_name, self.font_medium, color, 200, y)

            # Current value
            current_value = options[self.current_values[i]]
            if isinstance(current_value, tuple):  # Color
                value_text = f"RGB{current_value}"
            else:
                value_text = str(current_value)

            self.draw_text(value_text, self.font_medium, color, 600, y)

            # Arrows
            if is_selected:
                self.draw_text("◀ ▶", self.font_medium, self.highlight_color, 500, y)

        # Instructions
        self.draw_text("Use ARROW KEYS to navigate and change values",
                      self.font_small, self.text_color,
                      self.screen_width // 2, self.screen_height - 100)
        self.draw_text("Press ESC to go back",
                      self.font_small, self.text_color,
                      self.screen_width // 2, self.screen_height - 50)

        self.update_animation()

class HighScoreMenu(Menu):
    """High scores menu screen"""

    def __init__(self, screen):
        super().__init__(screen)
        self.high_scores_file = "high_scores.json"
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """Load high scores from file"""
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f)
        except IOError:
            pass

    def add_score(self, score, level):
        """Add new score to high scores"""
        self.high_scores.append({"score": score, "level": level})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        self.save_high_scores()

    def handle_event(self, event):
        """Handle high scores events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
        return None

    def draw(self):
        """Draw high scores menu"""
        self.screen.fill(self.background_color)

        # Title
        self.draw_text("HIGH SCORES", self.font_large, self.highlight_color,
                      self.screen_width // 2, 100)

        # High scores
        if not self.high_scores:
            self.draw_text("No scores yet!", self.font_medium, self.text_color,
                          self.screen_width // 2, 300)
        else:
            start_y = 200
            for i, score_data in enumerate(self.high_scores):
                y = start_y + i * 40
                rank = i + 1
                score = score_data["score"]
                level = score_data["level"]

                # Rank
                self.draw_text(f"{rank}.", self.font_medium, self.text_color, 200, y)

                # Score
                self.draw_text(f"{score:06d}", self.font_medium, self.highlight_color, 300, y)

                # Level
                self.draw_text(f"Level {level}", self.font_medium, self.text_color, 500, y)

        # Instructions
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