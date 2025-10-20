"""
Configuration file for Snake Game
Contains all game settings, colors, and constants
"""

import json
import os

# Default game settings
DEFAULT_CONFIG = {
    "screen": {
        "width": 600,
        "height": 400,
        "fps": 10
    },
    "game": {
        "block_size": 20,
        "initial_speed": 10
    },
    "colors": {
        "background": [0, 0, 0],
        "snake": [0, 255, 0],
        "snake_head": [0, 200, 0],
        "food_normal": [255, 0, 0],
        "food_special": [255, 255, 0],
        "food_bad": [128, 0, 128],
        "obstacle": [100, 100, 100],
        "powerup_slow": [255, 165, 0],
        "powerup_wall": [128, 128, 128],
        "text": [255, 255, 255],
        "text_highlight": [255, 255, 0]
    },
    "food": {
        "normal_score": 10,
        "special_score": 50,
        "bad_penalty": 1,
        "special_spawn_chance": 0.1
    },
    "powerups": {
        "slow_duration": 3000,   # 3 seconds
        "wall_duration": 5000,   # 5 seconds
        "spawn_chance": 0.005
    },
    "levels": {
        "max_level": 5,  # Maximum level available
        "obstacle_count": [1, 2, 4, 6, 8],
        "speed_multiplier": [1.0, 1.2, 1.5, 1.8, 2.0],
        "special_food_chance": [0.1, 0.15, 0.2, 0.25, 0.3],
        "level_names": ["Easy", "Normal", "Hard", "Expert", "Master"]
    }
}

class Config:
    """Configuration manager for the game"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with default config to ensure all keys exist
                return self._merge_configs(DEFAULT_CONFIG, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using default settings.")
                return DEFAULT_CONFIG.copy()
        else:
            return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def _merge_configs(self, default, user):
        """Merge user config with default config"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key_path, default=None):
        """Get configuration value using dot notation (e.g., 'screen.width')"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
    
    def get_color(self, color_name):
        """Get color tuple from config"""
        color = self.get(f"colors.{color_name}")
        return tuple(color) if color else (255, 255, 255)
    
    def get_screen_size(self):
        """Get screen dimensions"""
        return (self.get("screen.width"), self.get("screen.height"))
    
    def get_fps(self):
        """Get FPS setting"""
        return self.get("screen.fps")
    
    def get_block_size(self):
        """Get block size"""
        return self.get("game.block_size")

# Global config instance
config = Config()
