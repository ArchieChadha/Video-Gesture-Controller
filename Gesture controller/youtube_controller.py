import pyautogui
import time
import logging

class YouTubeController:
    def __init__(self):
        """Initialize the YouTube controller"""
        # Ensure PyAutoGUI fails safely
        pyautogui.FAILSAFE = True
        
        # Command mapping
        self.commands = {
            "Play": self.play,
            "Pause": self.pause,
            "Volume Up": self.volume_up,
            "Volume Down": self.volume_down,
            "Next Video": self.next_video,
            "Previous Video": self.previous_video
        }
        
        # Cooldown mechanism to prevent rapid-fire commands
        self.last_command_time = 0
        self.cooldown_duration = 1.5  # seconds
    
    def execute_command(self, gesture):
        """
        Execute a YouTube command based on the detected gesture
        
        Args:
            gesture: The detected gesture as a string
        """
        # Check if the command is valid and cooldown has expired
        current_time = time.time()
        if gesture in self.commands and (current_time - self.last_command_time) >= self.cooldown_duration:
            logging.debug(f"Executing command: {gesture}")
            self.last_command_time = current_time
            self.commands[gesture]()
    
    def play(self):
        """Play the video by pressing the space bar"""
        pyautogui.press('space')
    
    def pause(self):
        """Pause the video by pressing the space bar"""
        pyautogui.press('space')
    
    def volume_up(self):
        """Increase volume by pressing the up arrow"""
        pyautogui.press('up')
    
    def volume_down(self):
        """Decrease volume by pressing the down arrow"""
        pyautogui.press('down')
    
    def next_video(self):
        """Go to the next video by pressing Shift+N"""
        pyautogui.hotkey('shift', 'n')
    
    def previous_video(self):
        """Go to the previous video by pressing Shift+P"""
        pyautogui.hotkey('shift', 'p')
