# Project Name

Handy

## First-time Installation and Launch

To run the project first tome, follow these steps:

1. Open Terminal and go to the directory where you want to clone the project
2. Clone the repository: `git clone https://github.com/weareunder/hendi.git` // `git clone git@github.com:weareunder/hendi.git`
2. Navigate to the cloned repository directory: `cd hendi`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Run the project: `python main.py`

## Subsequent Launches

To run the project after the initial setup:

1. Navigate to the cloned repository directory: `cd hendi`
2. Checkout to the dev branch: `git checkout dev`
3. Pull updates: `git pull origin dev`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Run the project: `python main.py`

## Codebase

- **additional/utils.py** — contains utility functions for hand tracking and gesture recognition. includes calculations for hand size, finger tip smoothing, state updates, and various visualization helpers.

- **api/hand_api.py** — implements the HandAPI class for hand detection and tracking. provides methods for processing hand landmarks, calculating hand information, and rendering hand visualizations.

- **api/surface_api.py** — implements the SurfaceAPI class for detecting and managing interactive surfaces. handles surface detection, locking, highlighting, and coordinate system visualization for gesture interactions.

- **core/state_manager.py** — handles the application's state management. defines different states for gesture recognition and provides methods for transitioning between states based on detected hand movements and interactions.

- **core/video_processor.py** — implements the VideoProcessor class for handling video input and processing. manages frame capture, hand detection, surface detection, and user interface rendering.

- **gestures/cursor_control.py** — implements the CursorControl class for translating hand movements into cursor actions. handles cursor movement, sensitivity adjustments, and smoothing for precise cursor control using hand gestures.

- **gestures/click_handler.py** — manages click detection and handling for gesture-based interactions. implements methods for detecting clicks.