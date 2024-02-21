from screen_animator import ScreenAnimator, log_setup

if __name__ == "__main__":
    # log_setup.setup_logging(logging_level="DEBUG")
    screen_animator = ScreenAnimator(input_file="inputs.toml", debug=True)
    screen_animator.run()
