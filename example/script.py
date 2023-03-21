from screen_animator import ScreenAnimator, log_setup

if __name__ == "__main__":
    # log_setup.setup_logging(logging_level="DEBUG", size_mb=20, bkp_count=5)
    screen_animator = ScreenAnimator(input_file="inputs.toml", debug=True)
    screen_animator.run()
