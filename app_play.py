from pynput.keyboard import Key, Controller
from computer_recorder.mouse_input import MouseInput
from computer_recorder.key_input import KeyInput
from computer_recorder.screen_input import ScreenInput
import tensorflow as tf
import numpy as np
import time


def main():

    # CONFIGURATION
    model_path = '/Users/keanuinterone/Projects/ComputerRecorder/Models/model_5.2.1.1.tflite'
    video_frame_segment_shape = (20, 256, 256, 3)
    key_threshold = 0.5
    fps=10

    # INITIALIZATION
    video_frame_segment = np.zeros(video_frame_segment_shape, dtype=np.float32)
    key_state = [0, 0, 0, 0]

    # ON CLICK
    def on_click(x, y):
        nonlocal recording_center
        nonlocal waiting_for_input

        print(f'Setting recording center to ({x}, {y})')
        recording_center = (x, y)
        waiting_for_input = False

    # ON ENTER KEY PRESSED
    def enter_key_pressed():
        nonlocal waiting_for_input
        waiting_for_input = False

    # ON ESC KEY PRESSED
    def esc_key_pressed():
        nonlocal waiting_for_input
        waiting_for_input = False

    # ON SCREENSHOT
    def on_screenshot(img):
        nonlocal keyboard
        nonlocal key_state
        nonlocal video_frame_segment
        nonlocal key_threshold
        nonlocal interpreter
        nonlocal input_details
        nonlocal output_details

        # Normalize and convert the new image
        image = (np.array(img) / 255.0).astype(np.float32)

        # Shift and place new image at the end of video_frame_segment
        video_frame_segment = np.roll(video_frame_segment, -1, axis=0)
        video_frame_segment[-1] = image

        # Run inference
        start_time = time.time()
        interpreter.set_tensor(input_details[0]['index'], [video_frame_segment])
        try:
            interpreter.invoke()
        except:
            return
        
        # Get output tensor
        raw_pred = interpreter.get_tensor(output_details[0]['index'])[0]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Inference Time : {elapsed_time:.4f} seconds")
        y = (raw_pred > key_threshold).astype(np.float32)
        print(y)

        # Push the keys!
        # Up
        if y[0] != key_state[0]:
            if y[0]:
                keyboard.press(Key.up)
                key_state[0] = 1
            else:
                keyboard.release(Key.up)
                key_state[0] = 0
        
        # Left
        if y[1] != key_state[1]:
            if y[1]:
                keyboard.press(Key.left)
                key_state[1] = 1
            else:
                keyboard.release(Key.left)
                key_state[1] = 0

        # Right
        if y[2] != key_state[2]:
            if y[2]:
                keyboard.press(Key.right)
                key_state[2] = 1
            else:
                keyboard.release(Key.right)
                key_state[2] = 0

        # Down
        if y[3] != key_state[3]:
            if y[3]:
                keyboard.press(Key.down)
                key_state[3] = 1
            else:
                keyboard.release(Key.down)
                key_state[3] = 0

    # LOAD THE MODEL
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # CREATE MOUSE INPUT TO GET RECORDING AREA CENTER
    mouse_input = MouseInput(
        on_click=on_click
        )
    mouse_input.start_listener()
    recording_center = None
    print('Click center of recording area')
    waiting_for_input = True

    # WAIT FOR ON CLICK TO GET CALLED TO SET RECORDING CENTER
    while waiting_for_input:
        pass

    # STOP MOUSE INPUT
    mouse_input.stop_listener()

    # CREATE KEY INPUT AND LISTEN FOR ENTER AND ESC
    key_input = KeyInput(
        enter_key_pressed=enter_key_pressed,
        exit_key_pressed=esc_key_pressed
    )
    key_input.start_listener()
    print('Hit Enter to start player, Esc to stop')
    waiting_for_input = True

    # WAIT FOR ENTER KEY TO START PLAYER
    while waiting_for_input:
        pass

    # CREATE KEY CONTROLLER
    keyboard = Controller()

    # CREATE THE SCREEN INPUT WITH THE RECORDING CENTER
    screen_input = ScreenInput(
        frame_size=256,
        frame_center=recording_center,
        fps=fps,
        on_screenshot=on_screenshot
    )
    screen_input.start_listener()
    print('Player Started...')
    waiting_for_input = True

    # WAIT FOR USER TO HIT ESC
    while waiting_for_input:
        pass

    # STOP SCREEN INPUT
    screen_input.stop_listener()
    print('Player stoped')

if __name__ == "__main__":
    main()
