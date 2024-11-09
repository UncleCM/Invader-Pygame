import pygame

class SoundController:
    def __init__(self):
        """Initialize the sound controller and load sound effects"""
        # Ensure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Load sound effects
        try:
            self.shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
            self.explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
            self.game_over_sound = pygame.mixer.Sound("assets/game_over.wav")
            
            # Set volume levels
            self.shoot_sound.set_volume(0.3)
            self.explosion_sound.set_volume(0.4)
            self.game_over_sound.set_volume(0.5)
            
            self.sound_enabled = True
            print("Sound effects loaded successfully!")
            
        except Exception as e:
            print(f"Failed to load sound effects: {e}")
            self.sound_enabled = False
            
    def play_shoot(self):
        """Play shooting sound effect"""
        if self.sound_enabled:
            self.shoot_sound.play()
            
    def play_explosion(self):
        """Play explosion sound effect"""
        if self.sound_enabled:
            self.explosion_sound.play()
            
    def play_game_over(self):
        """Play game over sound effect"""
        if self.sound_enabled:
            self.game_over_sound.play()
            
    def cleanup(self):
        """Clean up sound resources"""
        try:
            pygame.mixer.quit()
        except:
            pass