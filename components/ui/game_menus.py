"""
Game-specific menu classes
"""

import pygame
import math
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
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(self.buttons):
                if button_rect.collidepoint(mouse_pos):
                    self.selected_option = i
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for i, button_rect in enumerate(self.buttons):
                    if button_rect.collidepoint(mouse_pos):
                        selected_action = self.options[i]
                        if selected_action == "Start Game":
                            return "Select Level"
                        return selected_action
        return None

    def draw(self):
        """Draw main menu"""
        self.screen.fill(self.background_color)

        # Title with animation and glow effect
        title_y = 150 + int(10 * math.sin(self.animation_timer * 0.05))
        
        # Draw title glow
        for offset in range(1, 4):
            glow_color = tuple(int(c * 0.3) for c in self.highlight_color)
            self.draw_text("SNAKE GAME", self.font_large, glow_color,
                          self.screen_width // 2 + offset, title_y + offset)
        
        # Main title
        self.draw_text("SNAKE GAME", self.font_large, self.highlight_color,
                      self.screen_width // 2, title_y, shadow=True)

        # Subtitle with pulse effect - fixed color handling
        subtitle_alpha = int(200 + 55 * math.sin(self.animation_timer * 0.03))
        if len(self.text_color) >= 3:
            subtitle_color = (*self.text_color[:3],)
        else:
            subtitle_color = self.text_color
        self.draw_text("Enhanced Edition", self.font_medium, subtitle_color,
                      self.screen_width // 2, title_y + 60, shadow=True)

        # Menu options
        start_y = 300
        button_width = 300
        button_height = 50
        button_spacing = 70

        self.buttons = []
        for i, option in enumerate(self.options):
            y = start_y + i * button_spacing
            is_selected = (i == self.selected_option)

            # Enhanced button colors
            base_color = (40, 40, 80) if not is_selected else (80, 80, 120)
            hover_color = (120, 120, 180)
            
            button_rect = self.draw_button(
                option,
                self.screen_width // 2 - button_width // 2,
                y,
                button_width,
                button_height,
                base_color,
                hover_color,
                is_selected
            )
            self.buttons.append(button_rect)

        # Instructions
        self.draw_text("Use ARROW KEYS or MOUSE to navigate, ENTER or CLICK to select",
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
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            start_y = 200
            level_height = 80
            for i in range(self.max_level):
                y = start_y + i * level_height
                box_width = 400
                box_height = 60
                box_x = self.screen_width // 2 - box_width // 2
                box_y = y - 10
                level_rect = pygame.Rect(box_x, box_y, box_width, box_height)
                if level_rect.collidepoint(mouse_pos):
                    self.selected_level = i
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                start_y = 200
                level_height = 80
                for i in range(self.max_level):
                    y = start_y + i * level_height
                    box_width = 400
                    box_height = 60
                    box_x = self.screen_width // 2 - box_width // 2
                    box_y = y - 10
                    level_rect = pygame.Rect(box_x, box_y, box_width, box_height)
                    if level_rect.collidepoint(mouse_pos):
                        return f"start_level_{i + 1}"
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

            # Enhanced box background with gradient
            if is_selected:
                # Gradient effect for selected level
                for i in range(box_height):
                    shade = int(120 - i * 0.5)
                    line_color = (shade, shade, shade + 20)
                    pygame.draw.line(self.screen, line_color, 
                                   (box_x, box_y + i), (box_x + box_width, box_y + i))
                border_color = (255, 255, 100)
                border_width = 3
            else:
                box_color = (60, 60, 80)
                pygame.draw.rect(self.screen, box_color, (box_x, box_y, box_width, box_height))
                border_color = (150, 150, 150)
                border_width = 2
            
            pygame.draw.rect(self.screen, border_color, (box_x, box_y, box_width, box_height), border_width)

            # Level name with shadow (centered in box)
            self.draw_text(level_name, self.font_medium, color,
                          self.screen_width // 2, y + 15, shadow=True)

        # Instructions
        self.draw_text("Use ARROW KEYS or MOUSE to select, ENTER or CLICK to start",
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
        self.selected_index = 0  # for keyboard navigation on buttons
        
        # Keep user's chosen snake color; no randomization here

        # Add score to high scores
        self.high_score_menu.add_score(final_score, level)

    def handle_event(self, event):
        """Handle game over events"""
        if self.show_high_score:
            return self._handle_high_score_event(event)
        
        if event.type == pygame.KEYDOWN:
            return self._handle_keyboard_event(event)
        elif event.type == pygame.MOUSEMOTION:
            # Update selection when hovering a button with mouse
            self._update_selection_from_mouse()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_event(event)
        
        return None
    
    def _handle_high_score_event(self, event):
        """Handle events when high score screen is shown"""
        result = self.high_score_menu.handle_event(event)
        if result == "back":
            self.show_high_score = False
        return result
    
    def _handle_keyboard_event(self, event):
        """Handle keyboard events"""
        key_actions = {
            pygame.K_r: "restart",
            pygame.K_m: "menu",
            pygame.K_q: "quit"
        }
        
        if event.key in key_actions:
            return key_actions[event.key]
        elif event.key == pygame.K_h:
            self.show_high_score = True
        elif event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % 4
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % 4
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            # Activate selected button
            return ["restart", "menu", "high_scores", "quit"][self.selected_index]
        
        return None
    
    def _handle_mouse_event(self, event):
        """Handle mouse click events (buttons and controls)"""
        if event.button != 1:  # Only handle left click
            return None

        mouse_pos = pygame.mouse.get_pos()

        # No FPS or screen size buttons on Game Over screen anymore

        # Check action buttons (recompute layout deterministically)
        x, start_y, button_width, button_height, spacing = self._button_layout()
        actions = [
            (pygame.Rect(x, start_y + 0 * (button_height + spacing), button_width, button_height), "restart"),
            (pygame.Rect(x, start_y + 1 * (button_height + spacing), button_width, button_height), "menu"),
            (pygame.Rect(x, start_y + 2 * (button_height + spacing), button_width, button_height), "high_scores"),
            (pygame.Rect(x, start_y + 3 * (button_height + spacing), button_width, button_height), "quit"),
        ]
        for rect, action in actions:
            if rect.collidepoint(mouse_pos):
                if action == "high_scores":
                    self.show_high_score = True
                    return None
                return action

        return None

    def draw(self):
        """Draw game over screen"""
        if self.show_high_score:
            self.high_score_menu.draw()
            return

        self.screen.fill(self.background_color)

        # Game Over text with enhanced animation
        game_over_y = 150 + int(5 * math.sin(self.animation_timer * 0.1))
        
        # Pulsing red effect
        red_intensity = int(200 + 55 * math.sin(self.animation_timer * 0.08))
        game_over_color = (red_intensity, 50, 50)
        
        # Draw with glow effect
        for offset in range(1, 3):
            glow_color = (red_intensity // 3, 20, 20)
            self.draw_text("GAME OVER", self.font_large, glow_color,
                          self.screen_width // 2 + offset, game_over_y + offset)
        
        self.draw_text("GAME OVER", self.font_large, game_over_color,
                      self.screen_width // 2, game_over_y, shadow=True)

        # Final score with highlight
        self.draw_text(f"Final Score: {self.final_score:06d}", self.font_medium, self.highlight_color,
                      self.screen_width // 2, 250, shadow=True)

        # Level reached
        self.draw_text(f"Level Reached: {self.level}", self.font_medium, self.text_color,
                      self.screen_width // 2, 300, shadow=True)

        # Options as clickable buttons (centered block)
        x, start_y, button_width, button_height, spacing = self._button_layout()

        mouse_pos = pygame.mouse.get_pos()
        # Unified button color scheme for visual consistency
        base_color = (70, 100, 160)
        hover_color = (100, 140, 200)
        button_specs = [
            ("Play Again", base_color, hover_color),
            ("Main Menu", base_color, hover_color),
            ("High Scores", base_color, hover_color),
            ("Quit", base_color, hover_color),
        ]
        for i, (label, base_color, hover_color) in enumerate(button_specs):
            y = start_y + i * (button_height + spacing)
            is_mouse_hover = pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos)
            is_selected = (i == self.selected_index)
            rect = self.draw_button(
                label,
                x,
                y,
                button_width,
                button_height,
                base_color,
                hover_color,
                is_hovered=(is_mouse_hover or is_selected)
            )

        # Instructions
        self.draw_text("Use UP/DOWN or MOUSE to select, ENTER/CLICK to confirm",
                       self.font_small, self.text_color,
                       self.screen_width // 2, self.screen_height - 70)
        self.draw_text("Shortcuts: R=Play Again, M=Menu, H=High Scores, Q=Quit",
                       self.font_small, self.text_color,
                       self.screen_width // 2, self.screen_height - 40)

        self.update_animation()

    def _update_selection_from_mouse(self):
        """Set selected_index based on current mouse hover over buttons."""
        x, start_y, button_width, button_height, spacing = self._button_layout()
        mouse_pos = pygame.mouse.get_pos()
        for i in range(4):
            y = start_y + i * (button_height + spacing)
            if pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos):
                self.selected_index = i
                break

    def _button_layout(self):
        """Compute consistent layout for action buttons and return (x, start_y, w, h, spacing)."""
        button_width = 320
        button_height = 52
        spacing = 16
        num = 4
        block_height = num * button_height + (num - 1) * spacing
        start_y = max(320, self.screen_height // 2 - block_height // 2 + 40)
        x = self.screen_width // 2 - button_width // 2
        return x, start_y, button_width, button_height, spacing