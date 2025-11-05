"""
Event handling for different game states
"""

import pygame

class EventHandler:
    """Handles events for different game states"""
    
    def __init__(self, game_state, menus, block_size):
        self.game_state = game_state
        self.menus = menus
        self.block_size = block_size
    
    def handle_events(self, snake=None):
        """Handle all game events"""
        for event in pygame.event.get():
            # Always check for QUIT first
            if event.type == pygame.QUIT:
                return False
            
            # Delegate to specific handlers
            result = None
            if self.game_state.state == "menu":
                result = self._handle_menu_events(event)
            elif self.game_state.state == "level_select":
                result = self._handle_level_select_events(event)
            elif self.game_state.state == "settings":
                result = self._handle_settings_events(event)
            elif self.game_state.state == "high_scores":
                result = self._handle_high_scores_events(event)
            elif self.game_state.state == "countdown":
                result = self._handle_countdown_events(event)
            elif self.game_state.state == "playing":
                result = self._handle_playing_events(event, snake)
            elif self.game_state.state == "paused":
                result = self._handle_paused_events(event)
            elif self.game_state.state == "game_over":
                result = self._handle_game_over_events(event)
            
            # If result is False (quit command), stop processing and return False
            if result is False:
                return False
            # If result is a tuple (start_level) or special string (restart, etc), return it
            if isinstance(result, tuple):
                return result
            if result in ["restart", "settings_changed"]:
                return result
        
        return True
    
    def _handle_menu_events(self, event):
        """Handle main menu events"""
        result = self.menus["main"].handle_event(event)
        if result == "Start Game":
            return "start_game"
        elif result == "Select Level":
            self.game_state.set_state("level_select")
        elif result == "Settings":
            self.game_state.set_state("settings")
        elif result == "High Scores":
            self.game_state.set_state("high_scores")
        elif result == "Quit":
            return False
        return True
    
    def _handle_level_select_events(self, event):
        """Handle level select events"""
        result = self.menus["level_select"].handle_event(event)
        if result and result.startswith("start_level_"):
            level = int(result.split("_")[2])
            return ("start_level", level)
        elif result == "back":
            self.game_state.set_state("menu")
        return True
    
    def _handle_settings_events(self, event):
        """Handle settings events"""
        result = self.menus["settings"].handle_event(event)
        if result == "back":
            self.game_state.set_state("menu")
            return "settings_changed"
        return True
    
    def _handle_high_scores_events(self, event):
        """Handle high scores events"""
        result = self.menus["high_scores"].handle_event(event)
        if result == "back":
            self.game_state.set_state("menu")
        return True
    
    def _handle_countdown_events(self, event):
        """Handle countdown events"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_state.set_state("menu")
        return True
    
    def _handle_playing_events(self, event, snake):
        """Handle playing state events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state.set_state("menu")
            elif event.key == pygame.K_SPACE:
                self.game_state.set_state("paused")
            elif snake:
                # Movement controls
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.change_direction(-self.block_size, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.change_direction(self.block_size, 0)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.change_direction(0, -self.block_size)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.change_direction(0, self.block_size)
        return True
    
    def _handle_paused_events(self, event):
        """Handle paused state events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game_state.set_state("playing")
            elif event.key == pygame.K_ESCAPE:
                self.game_state.set_state("menu")
        return True
    
    def _handle_game_over_events(self, event):
        """Handle game over events"""
        result = self.menus["game_over"].handle_event(event)
        if result == "restart":
            return "restart"
        elif result == "menu":
            self.game_state.set_state("menu")
        elif result == "quit":
            return False
        return True