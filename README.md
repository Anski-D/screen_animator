## Screen_Animator
`Screen_Animator` is a Python package to generate animated messages and images on a screen, with a focus on the Raspberry Pi.

The package uses an input and image files to generate messages that scroll right-to-left, and images that will randomly position themselves in the background, all while the colors continually change.

`Screen_Animator` makes extensive use of the Pygame Community Edition (`pygame-ce`) package.

## Prerequisites

Consider the following before using the app:
* You have a machine which supports graphical output.
* You have an appropriate operating system. The app is primarily designed for use on a Raspberry Pi, but will work on Linux or Windows PCs.
* You have Python version 3.10 or higher.
* You have read the guidance for using the app, below.

## Installation
It is recommended you install `Screen_Animator` into its own virtual environment. Guidance on setting up virtual environments is available online.

Then install the package:

```commandline
pip install git+https://github.com/Anski-D/screen_animator.git
```

Alternatively, you can clone the package and deal with it as you wish.

### Additional dependencies on Raspberry Pi

You might find additional dependencies are required on Raspberry Pi OS (as well as other Linux distributions). Install the additional dependencies by [following the `pygame-ce` compilation docs on GitHub](https://github.com/pygame-community/pygame-ce/wiki/Compiling-on-Linux).

> [!NOTE]
> Installing the dependencies should be enough, cloning and building `pygame-ce` should not be necessary.

## Usage
If the package is installed as recommended above, a command line script will be available that will copy an example `inputs.toml` file into your current directory.

Simply run:

```commandline
copy_examples
```

[Further information for specifying inputs in `inputs.toml` is provided.](#inputstoml)

The app can then be used by simply running, in the activated virtual environment:

```commandline
screen_animator
```

The following options can also be specified:

`-i, --input`
: Optional, default is `inputs.toml`. The location of the `TOML` file that contains the settings for the package.

`-r, --rotate`
: Optional flag, off by default. Sets whether the entire rendered animation should be rotated 180&deg;.

> [!NOTE]
> Some Raspberry Pi displays might need to be rotated 180&deg;. This can be done within Raspberry Pi OS configuration files, but setting this parameter in Python tends to give a much smoother animation.

`-f, --fps`
: Optional flag, off by default. When turned on, a small frames-per-second (FPS) counter is displayed. Useful for finding how high the FPS can be raised.

`-d, --debug`
: Optional flag, off by default. When turned on, animation is put in a 800x480 window, and the FPS counter is turned on (regardless of the setting above). Does not alter any logging levels.

`-l, --logging`
: Optional, off by default. No logging (other than minimal to the console) will occur unless specified. Once specified, logging will occur to a local log file. Examples include `INFO` or `DEBUG`.

### `inputs.toml`
This `TOML` file is used as an input to the main `ScreenAnimator` class. All settings are required or the input validation will fail, and are explained below.

> [!NOTE]
> The input file does not need to be called `inputs.toml`, as long the name matches the name provided to the `ScreenAnimator` class.

`colors`
: A list of colors to use in the background and text. Each color should be provided as a list of red-green-blue (RGB). At least two colors are required to prevent the package getting stuck in a loop.

`messages`

* `messages`
: A list of messages to scroll across the screen. A message will be chosen at random once the previous message is fully emerged from the right-hand side of the screen.

* `separator`
: A character string that will be appended to the end of the randomly-selected message to separate it from the next randomly-selected message.

* `typeface`
: The typeface to be used from the scrolling message. This should be a typeface installed on the system otherwise a fallback will be used.

* `sizes`
: A list of two integers to define the range of heights that should be used for the scrolling message. Each message will have a random height between the defined limits, and each message will be different from the last. To have messages at a constant height, set both numbers to the same value.

* `bold`
: A boolean defining whether the typeface used should be bold or not.

* `italic`
: A boolean defining whether the typeface used should be italic or not.

* `anti-aliasing`
: A boolean defining whether the text in the scrolling message should be rendered with antialiasing or not. While antialiasing will look better, it can cause significant lag and/or stuttering on devices such as a Raspberry Pi.

* `scroll_speed`
: Speed at which the text should scroll from right to left in pixels-per-second.

* `outline_width`
: The thickness in pixels to have as an outline around the rendered letters in the scrolling message. Helps separate the text from the background. Set to `0` to turn off.

* `outline_copies`
: Text outlines are copies of the message, rendered behind the main text. More copies looks better, but too many can cause lag/stuttering. Can also be set to `0` to turn off outline.

* `outline_colors`
: A list of colors to use as the outline. Each color should be provided as a list of RGB. At least one color should be provided, even if the `outline_width` or `outline_copies` is set to `0`,

* `start_middle`
: A boolean to set whether the scrolling message should always be centered vertically on the screen or can be positioned anywhere vertically.

`images`

* `sources`
: Image source listed as a pair with a required width value. `SVG` vector graphic formats can be used as well as raster formats such as `PNG` and `BMP`. A width value of `-1` with a raster format will use the original image size. Raster resizing will preserve the aspect ratio of the image, but might cause loss of quality.

* `number`
: Number of each image to render on the screen.

* `reposition_attempts`
: Integer value determines how many times the package should try to position all the images randomly to prevent overlaps. When there are a lot of images and/or images are large, this can be difficult. This value limits how many times the package will try to avoid overlaps for each image before moving on to the next. Negative values place no limit and could cause the animation to become stuck. Large values could cause the animations to periodically stall or essentially become stuck. Low values might result in some image overlap. A value of `0` allows uncontrolled overlap.

`timings`

* `fps`
: Sets the FPS target for the animation to run out. The target keeps the animations running smoothly, but too high a value might not be achievable and could cause scroll-speed inconsistencies. Low values could cause a stuttering effect.

* `image_change_time`
: Time in seconds between changes in image positioning.

* `color_change_time`
: Time in seconds between changes in color. This will only change background and text color, not outline. Color changes might not always be apparent due to the way random selections work.

## Contact

Contact me at <dave.anski@gmail.com>.

## License

This project uses the following license: [MIT](https://github.com/Anski-D/screen_animator/blob/main/LICENSE)
