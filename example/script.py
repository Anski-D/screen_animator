from screen_animator import ScreenAnimator, log_setup

INPUT_FILE = "inputs.toml"
FLIPPED = False
FPS_ON = False
DEBUG = False

if __name__ == "__main__":
    # log_setup.setup_logging(logging_level="DEBUG")
    screen_animator = ScreenAnimator(
        input_file=INPUT_FILE,
        flipped=FLIPPED,
        fps_on=FPS_ON,
        debug=DEBUG,
    )
    screen_animator.run()
