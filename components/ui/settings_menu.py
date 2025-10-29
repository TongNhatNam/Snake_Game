"""
Settings menu for game configuration
"""

import pygame
from .base_menu import Menu
from ..core import config

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