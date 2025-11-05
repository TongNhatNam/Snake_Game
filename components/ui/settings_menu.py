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
            ("Snake Color", "colors.snake", [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)])
        ]
        self.current_values = []
        self.load_current_values()
        # Button rects per setting: list of tuples (left_rect, right_rect)
        self._button_rects = []
        # Row rects for hover/selection
        self._row_rects = []

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                # Check click on any left/right button
                for i, pair in enumerate(self._button_rects):
                    if not pair:
                        continue
                    left_rect, right_rect = pair
                    if left_rect and left_rect.collidepoint(mouse_pos):
                        self.selected_setting = i
                        self.current_values[i] = max(0, self.current_values[i] - 1)
                        self.update_setting()
                        return None
                    if right_rect and right_rect.collidepoint(mouse_pos):
                        self.selected_setting = i
                        setting_name, key_path, options = self.settings[i]
                        self.current_values[i] = min(len(options) - 1, self.current_values[i] + 1)
                        self.update_setting()
                        return None
                # Click a row selects it
                for i, row in enumerate(self._row_rects):
                    if row and row.collidepoint(mouse_pos):
                        self.selected_setting = i
                        return None
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Hovering a row updates selection for better UX
            for i, row in enumerate(self._row_rects):
                if row and row.collidepoint(mouse_pos):
                    self.selected_setting = i
                    break
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

        # Layout metrics
        row_count = len(self.settings)
        row_height = 64
        panel_padding_y = 30
        panel_padding_x = 28
        vertical_gap = 8

        # Dynamic panel sizing, centered
        panel_width = min(760, max(520, self.screen_width - 120))
        panel_height = panel_padding_y * 2 + row_count * row_height + (row_count - 1) * vertical_gap
        panel_x = int((self.screen_width - panel_width) // 2)
        panel_y = int(max(70, (self.screen_height - panel_height) // 2 - 20))
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # Panel visuals
        panel_bg = (26, 28, 36)
        panel_border = (120, 120, 160)
        pygame.draw.rect(self.screen, panel_bg, panel_rect, 0, border_radius=12)
        pygame.draw.rect(self.screen, panel_border, panel_rect, 2, border_radius=12)

        # Title
        self.draw_text("SETTINGS", self.font_large, self.highlight_color,
                      self.screen_width // 2, panel_y - 28)

        # Settings
        start_y = panel_y + panel_padding_y
        setting_height = row_height
        row_left = panel_x + panel_padding_x
        # Two-column layout: name on left, controls on right
        name_x = row_left
        controls_right = panel_x + panel_width - panel_padding_x

        # Reset button/row rects for this frame
        self._button_rects = []
        self._row_rects = []

        mouse_pos = pygame.mouse.get_pos()

        for i, (setting_name, key_path, options) in enumerate(self.settings):
            y = start_y + i * (setting_height + vertical_gap)
            is_selected = (i == self.selected_setting)
            # Row background
            row_rect = pygame.Rect(panel_x + 10, int(y + (row_height - 44) // 2), panel_width - 20, 44)
            if is_selected:
                row_color = (58, 62, 88)
                pygame.draw.rect(self.screen, row_color, row_rect, 0, border_radius=8)
                pygame.draw.rect(self.screen, (255, 255, 140), row_rect, 2, border_radius=8)
            else:
                row_color = (40, 44, 60) if i % 2 == 0 else (36, 40, 56)
                pygame.draw.rect(self.screen, row_color, row_rect, 0, border_radius=8)
                pygame.draw.rect(self.screen, (90, 96, 128), row_rect, 1, border_radius=8)
            self._row_rects.append(row_rect)

            # Setting name (left-aligned, vertically centered in row)
            color = self.highlight_color if is_selected else self.text_color
            name_y = int(y + row_height / 2 - self.font_medium.get_height() / 2)
            self.draw_text(setting_name, self.font_medium, color, name_x, name_y, center=False)

            # Current value
            current_value = options[self.current_values[i]]
            is_color_setting = (key_path == "colors.snake")
            if isinstance(current_value, tuple) and not is_color_setting:
                value_text = f"RGB{current_value}"
            else:
                value_text = str(current_value) if not isinstance(current_value, tuple) else ""

            # Controls area (right aligned)
            pill_width = 180
            pill_height = 34
            spacing = 12
            right_y = int(y + row_height/2 - pill_height/2)

            # Left and right buttons
            btn_w = 36
            btn_h = pill_height
            left_rect = pygame.Rect(controls_right - (btn_w + spacing + pill_width + spacing + btn_w), right_y, btn_w, btn_h)
            right_rect = pygame.Rect(controls_right - btn_w, right_y, btn_w, btn_h)
            pill_rect = pygame.Rect(controls_right - (btn_w + spacing + pill_width), right_y, pill_width, pill_height)

            # Pill background
            pygame.draw.rect(self.screen, (18, 20, 28), pill_rect, 0, border_radius=10)
            pygame.draw.rect(self.screen, (170, 176, 200), pill_rect, 1, border_radius=10)

            # Color swatch: for snake color, show swatch only (no RGB text)
            if isinstance(current_value, tuple):
                sw = 18
                swatch = pygame.Rect(pill_rect.left + 10, pill_rect.top + (pill_height - sw)//2, sw, sw)
                pygame.draw.rect(self.screen, current_value, swatch, 0, border_radius=4)
                pygame.draw.rect(self.screen, (230, 230, 230), swatch, 1, border_radius=4)
                if not is_color_setting and value_text:
                    self.draw_text(value_text, self.font_small, color, swatch.right + 8 + (pill_rect.width - sw - 18)//2, pill_rect.centery)
            else:
                self.draw_text(value_text, self.font_medium, color, pill_rect.centerx, pill_rect.centery)

            # Draw left/right buttons for this setting

            # Button appearance
            left_hover = left_rect.collidepoint(mouse_pos)
            right_hover = right_rect.collidepoint(mouse_pos)
            left_color = (96, 104, 150) if (is_selected or left_hover) else (70, 74, 104)
            right_color = (96, 104, 150) if (is_selected or right_hover) else (70, 74, 104)

            pygame.draw.rect(self.screen, left_color, left_rect, 0, border_radius=8)
            pygame.draw.rect(self.screen, right_color, right_rect, 0, border_radius=8)
            pygame.draw.rect(self.screen, (220, 226, 255), left_rect, 2, border_radius=8)
            pygame.draw.rect(self.screen, (220, 226, 255), right_rect, 2, border_radius=8)

            # Draw arrow icons (vector chevrons, no font dependency)
            self._draw_chevron(self.screen, left_rect, direction="left", color=(255, 255, 255))
            self._draw_chevron(self.screen, right_rect, direction="right", color=(255, 255, 255))

            # Save rects for event handling
            self._button_rects.append((left_rect, right_rect))

        # Instructions
        self.draw_text("Click ◀ ▶ to adjust | Arrow keys navigate | ESC back",
                      self.font_small, self.text_color,
                      self.screen_width // 2, panel_y + panel_height + 24)

        self.update_animation()

    def _draw_chevron(self, surface, rect, direction="left", color=(255, 255, 255)):
        """Draw a chevron icon inside rect using polygons (font-independent)."""
        try:
            cx, cy = rect.centerx, rect.centery
            w = max(8, rect.width // 3)
            h = max(10, rect.height // 2)
            if direction == "left":
                points = [(cx + w//2, cy - h//2), (cx - w//2, cy), (cx + w//2, cy + h//2)]
            else:  # right
                points = [(cx - w//2, cy - h//2), (cx + w//2, cy), (cx - w//2, cy + h//2)]
            pygame.draw.polygon(surface, color, points)
        except Exception:
            # Fallback to simple text if polygon fails
            arrow = "<" if direction == "left" else ">"
            self.draw_text(arrow, self.font_medium, color, rect.centerx, rect.centery)