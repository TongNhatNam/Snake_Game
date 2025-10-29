"""
Game state management
"""

class GameState:
    """Manages game state and transitions"""
    
    def __init__(self):
        self.state = "menu"  # menu, playing, paused, game_over, countdown, level_select, settings, high_scores
        self.level = 1
        self.score = 0
        self.high_score = 0
        
        # Timers
        self.snake_move_timer = 0
        self.snake_move_interval = 200
        self.countdown_timer = 0
        self.countdown_duration = 3000
        
        # Game area
        self.game_area_width = 400
        self.game_area_height = 400
        self.game_area_x = 50
        self.game_area_y = 50
    
    def set_state(self, new_state):
        """Change game state"""
        self.state = new_state
    
    def is_playing(self):
        """Check if currently playing"""
        return self.state == "playing"
    
    def is_paused(self):
        """Check if game is paused"""
        return self.state == "paused"
    
    def reset_for_new_game(self, level=1):
        """Reset state for new game"""
        self.level = level
        self.score = 0
        self.snake_move_timer = 0
        self.countdown_timer = 0