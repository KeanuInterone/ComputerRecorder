from computer_recorder.input_recorder import InputRecorder


def main():
    def on_enter_pressed():
        nonlocal input_recorder
        print('Starting recorder...')
        input_recorder.start_new_recording()
        print('Recording Started...')

    def on_esc_pressed():
        nonlocal input_recorder
        input_recorder.stop_recording()
        print('Recording Finished')
        input_recorder.save_recording('/Users/keanuinterone/Projects/ComputerRecorder/Recordings')
        nonlocal is_running
        is_running = False

    is_running = True
    input_recorder = InputRecorder(
        record_keys=True,
        record_screen=True,
        screen_input_fps=10,
        enter_key_pressed=on_enter_pressed,
        esc_key_pressed=on_esc_pressed
        )

    print('Hit Enter to record, and esc to stop')

    while is_running:
        pass

if __name__ == "__main__":
    main()