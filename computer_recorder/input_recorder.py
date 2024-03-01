from .key_input import KeyInput

##################
# INPUT RECORDER #
##################


# CLASS
class InputRecorder:

    # INITIALIZE
    def __init__(
            self,
            record_keys=False,
            record_screen=False,
            enter_key_pressed=None,
            esc_key_pressed=None
            ):
        
        # Instance variables
        self.record_keys = record_keys
        self.record_screen = record_screen

        # Key input
        self.key_input = KeyInput(
            key_pressed=self.key_pressed,
            key_released=self.key_released,
            enter_key_pressed=enter_key_pressed,
            exit_key_pressed=esc_key_pressed
        )
        self.key_input.start_listener()

        # Is recording flag
        self.is_recording = False

        # The event log
        self.events = []


    # START NEW RECORDING
    def start_new_recording(self):
        # Reset event list
        self.events = []

        # Flip recording flag
        self.is_recording = True


    #STOP RECORDING
    def stop_recording(self):

         # Flip recording flag
        self.is_recording = False


    # ON KEY PRESSED
    def key_pressed(self, key):
        # If we are not recording and not recording keys...
        if not self.is_recording and not self.record_keys:
            # ... don't log anything
            return
        
        # Add the event to the event list
        self.events.append(f'{key} pressed')
        
            

    # ON KEY RELEASED
    def key_released(self, key):
        # If we are not recording and not recording keys......
        if not self.is_recording and not self.record_keys:
            # ... don't log anything
            return
        
        # Add the event to the event list
        self.events.append(f'{key} released')

    
    # ON SAVE
    def save_recording(self, location):
        # Implement saving logic here
        print(self.events)
        pass  # Placeholder for saving logic
