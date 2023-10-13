## AirTouchBar for Mac

## Overview

AirTouchBar allows you to control your MacBook's Touch Bar using hand gestures. Built on Python and MediaPipe, it uses computer vision to recognize hand movements and translate them into Touch Bar actions.

## Usage
when the application starts, different hand gesture indicates different touchbar actions.

- Closed fist - play/pause music
- pinch hand - adjust volume
- palm facing left - last track
- palm facing right - next track

## Demo

[Watch the video on YouTube](https://www.youtube.com/watch?v=_3HRL63dFGE)




## Requirements

- Python 3.8+
- MediaPipe
- OpenCV

## Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/yourusername/AirTouchBar-for-mac.git

# Change into the project directory
cd AirTouchBar-for-mac

# Install dependencies
pip install -r requirements.txt
\`\`\`

## Usage

1. Run the main script:

    \`\`\`bash
    python src/main.py
    \`\`\`

2. Perform hand gestures near the camera to control the Touch Bar.

## Configuration

You can modify settings like `max_hands`, `detection_confidence`, and `tracking_confidence` in the `hand_detector.py` file.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
