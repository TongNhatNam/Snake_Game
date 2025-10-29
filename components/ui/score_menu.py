"""
High score menu and management
"""

import json
import os
import pygame
from .base_menu import Menu

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