# project name

handy

## first-time installation and launch

to run the project first tome, follow these steps:

1. open terminal and go to the directory where you want to clone the project
2. clone the repository: `git clone https://github.com/weareunder/hendi.git` // `git clone git@github.com:weareunder/hendi.git`
2. navigate to the cloned repository directory: `cd hendi`
3. create a virtual environment: `python -m venv venv`
4. activate the virtual environment: `source venv/bin/activate`
5. install the required dependencies: `pip install -r requirements.txt`
6. run the project: `python main.py`

## subsequent launches

to run the project after the initial setup:

1. navigate to the cloned repository directory: `cd hendi`
2. checkout to the dev branch: `git checkout dev`
3. pull updates: `git pull origin dev`
4. activate the virtual environment: `source venv/bin/activate`
5. install the required dependencies: `pip install -r requirements.txt`
6. run the project: `python main.py`

## codebase

- **additional/utils.py** — contains utility functions for hand tracking and gesture recognition. includes calculations for hand size, finger tip smoothing, state updates, and various visualization helpers.

- **api/hand_api.py** — implements the handapi class for hand detection and tracking. provides methods for processing hand landmarks, calculating hand information, and rendering hand visualizations.

- **api/surface_api.py** — implements the surfaceapi class for detecting and managing interactive surfaces. handles surface detection, locking, highlighting, and coordinate system visualization for gesture interactions.

- **core/state_manager.py** — handles the application's state management. defines different states for gesture recognition and provides methods for transitioning between states based on detected hand movements and interactions.

- **core/video_processor.py** — implements the videoprocessor class for handling video input and processing. manages frame capture, hand detection, surface detection, and user interface rendering.

- **gestures/cursor_control.py** — implements the cursorcontrol class for translating hand movements into cursor actions. handles cursor movement, sensitivity adjustments, and smoothing for precise cursor control using hand gestures.

- **gestures/click_handler.py** — manages click detection and handling for gesture-based interactions. implements methods for detecting clicks.

## documentation

for detailed documentation about the project, including api references, usage guides, and development guidelines, please visit our [documentation page](https://handy.vision/docs) (work in progress).