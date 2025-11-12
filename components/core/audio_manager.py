"""
Audio Manager for Snake Game
Handles background music and sound effects
"""

import pygame
import os
from .config import config

class AudioManager:
    """Manages all audio in the game"""
    
    def __init__(self):
        """Initialize audio system"""
        self.sounds = {}
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.music_enabled = True
        self.sound_enabled = True
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.audio_available = True
        except pygame.error:
            self.audio_available = False
            return
        
        # Load sounds
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound files"""
        if not self.audio_available:
            return
        
        sound_files = {
            'death': 'lose.mp3'
        }
        
        sounds_dir = os.path.join('assets', 'sounds')
        
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(sounds_dir, filename)
            try:
                if os.path.exists(filepath):
                    sound = pygame.mixer.Sound(filepath)
                    sound.set_volume(self.sound_volume)
                    self.sounds[sound_name] = sound
            except pygame.error:
                pass  # Skip if sound can't be loaded
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.audio_available or not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error:
                pass
    
    def play_music(self, music_file=None):
        """Play background music"""
        if not self.audio_available or not self.music_enabled:
            return
        
        if music_file is None:
            music_file = os.path.join('assets', 'sounds', 'background_music.mp3')
        
        try:
            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
        except pygame.error:
            pass
    
    def stop_music(self):
        """Stop background music"""
        if self.audio_available:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.audio_available:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except pygame.error:
                pass
    
    def set_sound_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.sound_volume)
            except pygame.error:
                pass
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        else:
            self.play_music()
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
    
    def is_music_enabled(self):
        """Check if music is enabled"""
        return self.music_enabled and self.audio_available
    
    def is_sound_enabled(self):
        """Check if sound effects are enabled"""
        return self.sound_enabled and self.audio_available

# Global audio manager instance
audio_manager = AudioManager()