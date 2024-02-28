import pytest
from pynput import keyboard
from ..computer_recorder.key_input import KeyInput
from ..computer_recorder.custom_exceptions.invalid_state_error import InvalidStateError

# Fixture to create a KeyInput instance
@pytest.fixture
def key_input_instance():
    return KeyInput()

# Test case for checking if attempting to stop the listener without creating one raises InvalidStateError
def test_raises_invalid_state_error_stop_listener(key_input_instance):
    with pytest.raises(InvalidStateError):
        key_input_instance.stop_listener()

# Test case for checking if the KeyInput instance can receive key press events
def test_can_receive_key_press_events(key_input_instance):
    key_pressed_callback_called = False

    def key_pressed_callback(key):
        nonlocal key_pressed_callback_called
        key_pressed_callback_called = True

    key_input_instance.key_pressed = key_pressed_callback

    # Emulate a key press event
    with keyboard.Listener(on_press=lambda key: key_input_instance.on_press(key)):
        key_input_instance.start_listener()

        # Simulate a key press event
        key_input_instance.on_press(keyboard.KeyCode.from_char('a'))

    assert key_pressed_callback_called

# Test case for checking if the KeyInput instance can receive key release events
def test_can_receive_key_release_events(key_input_instance):
    key_released_callback_called = False

    def key_released_callback(key):
        nonlocal key_released_callback_called
        key_released_callback_called = True

    key_input_instance.key_released = key_released_callback

    # Emulate a key release event
    with keyboard.Listener(on_release=lambda key: key_input_instance.on_release(key)):
        key_input_instance.start_listener()

        # Simulate a key release event
        key_input_instance.on_release(keyboard.KeyCode.from_char('a'))

    assert key_released_callback_called
