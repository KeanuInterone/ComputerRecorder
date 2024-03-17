from pynput.keyboard import Key, Controller
from computer_recorder.mouse_input import MouseInput
from computer_recorder.key_input import KeyInput
from computer_recorder.screen_input import ScreenInput
import tensorflow as tf
#import tensorflow_hub as hub
import numpy as np
# from tensorflow.python.framework.ops import disable_eager_execution
# disable_eager_execution()

def main():

    def on_click(x, y):
        nonlocal recording_center
        nonlocal waiting_for_input

        print(f'Setting recording center to ({x}, {y})')
        recording_center = (x, y)
        waiting_for_input = False

    def enter_key_pressed():
        nonlocal waiting_for_input
        waiting_for_input = False

    def esc_key_pressed():
        nonlocal waiting_for_input
        waiting_for_input = False


    video_input = np.array([np.zeros((20, 256, 256, 3))], dtype=np.float32)
    action_input = np.array([np.zeros((19, 4))], dtype=np.float32)
    key_state = [0, 0, 0, 0]
    def on_screenshot(img):
        nonlocal keyboard
        nonlocal infer
        nonlocal key_state
        nonlocal video_input
        nonlocal action_input

        image = (np.array(img) / 255.0).astype(np.float32)
        video_input[0] = np.roll(video_input[0], -1)
        video_input[0][19] = image
        

        result = infer(video_input=tf.constant(video_input), action_input=tf.constant(action_input))
        y = (np.array(result['dense'][0]) > 0.5).astype(np.float32)
        print(y)

        action_input[0] = np.roll(action_input[0], -1)
        action_input[0][18] = y

        print("VIDEO INPUT!!!!")
        print(video_input)
        print("ACTION_INPUT!!!")
        print(action_input)

        # Up
        if y[0] != key_state[0]:
            if y[0]:
                print('Up!')
                keyboard.press(Key.up)
                key_state[0] = 1
            else:
                keyboard.release(Key.up)
                key_state[0] = 0
        
        # Left
        if y[1] != key_state[1]:
            if y[1]:
                print('Left!')
                keyboard.press(Key.left)
                key_state[1] = 1
            else:
                keyboard.release(Key.left)
                key_state[1] = 0

        # Right
        if y[2] != key_state[2]:
            if y[2]:
                print('Right!')
                keyboard.press(Key.right)
                key_state[2] = 1
            else:
                keyboard.release(Key.right)
                key_state[2] = 0

        # Down
        if y[3] != key_state[3]:
            if y[3]:
                print('Down!')
                keyboard.press(Key.down)
                key_state[3] = 1
            else:
                keyboard.release(Key.down)
                key_state[3] = 0

    # LOAD THE MODEL
    #model = tf.keras.models.load_model('/Users/keanuinterone/Projects/ComputerRecorder/Models/model_2.0.2.keras')
    # with open('/Users/keanuinterone/Projects/ComputerRecorder/Models/model_2.0.2_architecture.json', 'r') as f:
    #     model = tf.keras.models.model_from_json(f.read(), custom_objects={'KerasLayer':hub.KerasLayer})
                
    model = tf.saved_model.load('/Users/keanuinterone/Projects/ComputerRecorder/Models/model_two')
    print(list(model.signatures.keys()))
    infer = model.signatures['serving_default']
                
    # model = tf.keras.models.load_model(
    #   ('/Users/keanuinterone/Projects/ComputerRecorder/Models/model_2.0.2.keras'),
    #    custom_objects={'KerasLayer':hub.KerasLayer}
    # )
    
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

    # LOAD MODEL
    # Build a new Keras model with the inference layer
    # video_input = tf.keras.layers.Input(shape=(20, 256, 256, 3), name='video_input')
    # action_input = tf.keras.layers.Input(shape=(19, 4), name='action_input')
    # inference_layer = tf.keras.layers.TFSMLayer(
    #     '/Users/keanuinterone/Projects/ComputerRecorder/Models/model_two', 
    #     call_endpoint='serving_default', 
    # )([video_input, action_input])
    # model = tf.keras.Model(inputs=[video_input, action_input], outputs=inference_layer)

    # video_input = tf.keras.layers.Input(shape=(20, 256, 256, 3), name='video_input')
    # action_input = tf.keras.layers.Input(shape=(19, 4), name='action_input')
    # inference_layer = hub.KerasLayer("/Users/keanuinterone/Projects/ComputerRecorder/Models/model_two")([video_input, action_input])
    # model = tf.keras.Model(inputs=[video_input, action_input], outputs=inference_layer)


    # CREATE THE SCREEN INPUT WITH THE RECORDING CENTER
    screen_input = ScreenInput(
        frame_size=256,
        frame_center=recording_center,
        fps=10,
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
