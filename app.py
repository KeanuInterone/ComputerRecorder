from computer_recorder.input_recorder import InputRecorder


def on_enter_pressed():
    input_recorder.start_new_recording()
    print('Recording Started...')

def on_esc_pressed():
    input_recorder.stop_recording()
    print('Recording Finished')
    input_recorder.save_recording('locations')
    is_running = False

is_running = True
input_recorder = InputRecorder(
    record_keys=True,
    enter_key_pressed=on_enter_pressed,
    esc_key_pressed=on_esc_pressed
    )

print('Hit Enter to record, and esc to stop')

while is_running:
    pass