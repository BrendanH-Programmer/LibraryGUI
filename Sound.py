# Import neccessary module
import pygame # Import the pygame module for multimedia applications

# Initialize the Pygame mixer module for sound playback
pygame.mixer.init()

# Load the click sound file
click_sound = pygame.mixer.Sound("click.wav")

class Sound:
    def play_click_sound():
        """
        Play the click sound.
        """
        # Use Pygame mixer to play the loaded click sound
        click_sound.play()