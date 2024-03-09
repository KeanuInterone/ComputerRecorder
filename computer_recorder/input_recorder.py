from .key_input import KeyInput
from .screen_input import ScreenInput
import pickle
import os
import time

##################
# INPUT RECORDER #
##################


# CLASS
class InputRecorder:
    """
    A class to initialize different recording types such as keys and screen
    """

    # INITIALIZE
    def __init__(
            self,
            record_keys=False,
            record_screen=False,
            screen_input_frame_size=256,
            screen_input_frame_center=(128, 128),
            screen_input_fps=60,
            enter_key_pressed=None,
            esc_key_pressed=None
            ):
        """
        Initializer for the Input Recorder class that gives you methods to start and stop recording
        of your key strokes and screen

        Args:
            record_keys (bool, optional): weather or not to record key strokes
            record_screen (bool, optional): weather or not to record screen
            screen_input_frame_size (int, optional): Size of one side of a square frame
            screen_input_frame_center (tuple (x, y), optional): Center of the square frame
            screen_input_fps (int, optional): Frames per second of recording
            enter_key_pressed (function, optional): Function that is called when enter key is pressed
            esc_key_pressed (function, optional): Function that is called when esc key is pressed
        """
        # Instance variables
        self.record_keys = record_keys
        self.record_screen = record_screen

        # Key input - create this so that we can listen to enter and esc key presses
        self.key_input = KeyInput(
            key_pressed=self.key_pressed,
            key_released=self.key_released,
            enter_key_pressed=enter_key_pressed,
            exit_key_pressed=esc_key_pressed
            )
        self.key_input.start_listener()

        # Screen Input
        self.screen_input = None
        if self.record_screen:
            self.screen_input = ScreenInput(
                frame_size=screen_input_frame_size,
                frame_center=screen_input_frame_center,
                fps=screen_input_fps,
                on_screenshot=self.on_screenshot
                )

        # Is recording flag
        self.is_recording = False

        # Recording logs
        self.key_stroke_events = []
        self.screen_video_frames = []


    # START NEW RECORDING
    def start_new_recording(self):
        """
        Resets current recorded events and video frames and starts a new recording.
        If
        """
        # Reset logs
        self.key_stroke_events = []
        self.screen_video_frames = []

        # If recording screen...
        if self.record_screen:
            # ... start the screen listener - start_listener just returns if already listening
            self.screen_input.start_listener()

        # Set is recording to true
        self.is_recording = True


    # STOP RECORDING
    def stop_recording(self):
        """
        Stops recording
        """
        # If recording screen...
        if self.record_screen:
            # ... stop the screen listener
            self.screen_input.stop_listener()

         # Flip recording flag
        self.is_recording = False


    # ON KEY PRESSED
    def key_pressed(self, key):
        """
        Callback for KeyInput, called whenever a key is pressed. Logs the event
        of a key press. Returns if not recording or not recording keys.
        """
        # If we are not recording or not recording keys...
        if not self.is_recording or not self.record_keys:
            # ... don't log anything
            return
        
        # Add the event to the event list
        self.key_stroke_events.append(f'{key} pressed')
        
            

    # ON KEY RELEASED
    def key_released(self, key):
        """
        Callback for KeyInput, called whenever a key is released. Logs the event
        of a key release. Returns if not recording or not recording keys.
        """
        # If we are not recording or not recording keys......
        if not self.is_recording or not self.record_keys:
            # ... don't log anything
            return
        
        # Add the event to the event list
        self.key_stroke_events.append(f'{key} released')


    # ON SCREENSHOT
    def on_screenshot(self, img):
        """
        Callback for ScreenInput. Called frames per second every second when ScreenInput
        is listening. Logs the image. Returns if not recording or recording screen

        ARGS:
            img (np.array): image of the specified area of the screen
        """
        # If we are not recording or not recording screen......
        if not self.is_recording or not self.record_screen:
            # ... don't log anything
            return
        
        # Add screenshot to screen recording
        self.screen_video_frames.append(img)

    
    # ON SAVE
    def save_recording(self, location):
        """
        Saves input from either key or screen input if specified from initialization.
        Saves as pkl files

        ARGS:
            location (string): directory to save recording bundle
        """
        # Create recording object
        recording = {}
        if self.record_keys:
            recording['key_input_events'] = self.key_stroke_events
        if self.record_screen:
            recording['video'] = self.screen_video_frames
        
        # Return if there is nothing recorded
        if not recording:
            return
        
        # Create the file name
        timestamp = int(time.time())
        filename = f"recording_{timestamp}.pickle"
        recording_path = os.path.join(location, filename)

        # Save recording to pickel file
        with open(recording_path, 'wb') as handle:
            pickle.dump(recording, handle, protocol=pickle.HIGHEST_PROTOCOL)
