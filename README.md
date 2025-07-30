# Eating Detection

A real-time object detection system that monitors camera feeds to detect specific objects (such as bottles, food items, etc.) and sends notifications when target objects are identified. The system uses YOLO (You Only Look Once) deep learning model for accurate object detection and provides a command-line interface for easy configuration and control.

## Features

- **Real-time Object Detection**: Uses YOLO model for fast and accurate detection
- **Configurable Detection Targets**: Specify which objects to detect (bottles, food items, etc.)
- **Adjustable Confidence Threshold**: Fine-tune detection sensitivity
- **Live Camera Integration**: Works with USB cameras and webcams
- **Notification System**: Socket-based notifications when objects are detected
- **Command-line Interface**: Easy-to-use CLI for configuration and control
- **Persistent Settings**: Configuration saved between sessions
- **Comprehensive Testing**: Fully tested with 33+ unit tests

## Architecture

The system consists of several key components:

- **Main Application** (`main.py`): Entry point that coordinates all components
- **Food Detection System** (`src/food_detection_system.py`): Manages YOLO model and detection logic
- **YOLO Wrapper** (`src/yolo.py`): Handles camera integration and object detection
- **Notification System** (`src/notification_system.py`): Manages alerts and messaging
- **Command-line Interface** (`src/cmd_app.py`): Provides user interaction capabilities
- **Notification Client** (`notification_client.py`): Standalone client to receive notifications

## Quick Start

### 1. Install Python

Make sure you have Python 3.8 or newer installed.

### 2. Clone the repository

```bash
git clone git@github.com:Enlightened-Monkey/eating-detection.git
cd eating-detection
```

### 3. Install dependencies

Install required libraries using pip:

```bash
pip3 install -r requirements.txt
```

### 4. Run the notification client (optional)

Open a new terminal and start the notification client to receive notifications when desired object is detected:

```bash
./notification_client.py
```

### 5. Run the main application

In another terminal, start the main program:

```bash
./main.py
```

### 6. Use the command-line interface

You can use the following commands in the application:

- `help` – Show available commands
- `start` – Start object detection. After first run model file yolo12l.pt will be automatically dowloaded into src/detectionmodels/ 
- `stop` – Stop object detection
- `what_to_detect` – Set objects to detect (comma-separated)
- `threshold` – Set detection confidence threshold (0.0–1.0)
- `camera_settings` – Configure camera resolution and frame check interval
- `exit` – Exit the application

### 7. Configuration

Settings are saved in `settings.json` in the root directory. You can edit this file manually or use the CLI commands.

**Available Configuration Options:**

```json
{
    "objects_to_detect": ["bottle", "apple", "banana"],
    "threshold": 0.5,
    "camera_settings": {
        "resolution": [640, 480],
        "frame_check_interval": 1
    },
    "user_ids": [1]
}
```

- **objects_to_detect**: Array of object names to detect (see YOLO class names)
- **threshold**: Detection confidence threshold (0.0-1.0, default: 0.5)
- **camera_settings**:
  - **resolution**: Camera resolution [width, height] (default: [640, 480])
  - **frame_check_interval**: Seconds between frame checks (default: 1)
- **user_ids**: Array of user IDs for notifications

## Troubleshooting

### Common Issues

**Camera not working:**
- Ensure your camera is not being used by another application
- Try different camera indices (0, 1, 2) if you have multiple cameras
- Check camera permissions on your system

**YOLO model download fails:**
- Ensure you have internet connectivity
- The model (yolo12l.pt) will be automatically downloaded on first run
- Manual download: Place the model file in `src/detectionmodels/`

**No objects detected:**
- Lower the detection threshold using the `threshold` command
- Ensure proper lighting and camera positioning
- Verify the object names are correct (use standard YOLO class names)

**Notification client not receiving messages:**
- Ensure the notification client is running before starting detection
- Check that ports 65432 is available
- Verify firewall settings if running on different machines

### Performance Tips

- Use lower resolutions for better performance: `camera_settings` → `640x480` or `320x240`
- Increase `frame_check_interval` to reduce CPU usage
- Ensure adequate lighting for better detection accuracy

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Project Structure

```
eating-detection/
├── main.py                    # Main application entry point
├── notification_client.py     # Standalone notification client
├── requirements.txt           # Python dependencies
├── settings.json             # Configuration file
├── src/                      # Source code
│   ├── cmd_app.py           # Command-line interface
│   ├── food_detection_system.py  # Detection system coordinator
│   ├── notification_system.py    # Notification handling
│   ├── yolo.py              # YOLO model wrapper
│   └── detectionmodels/     # Model files (auto-created)
└── tests/                   # Unit tests
    ├── test_CmdApp.py
    ├── test_FoodDetectionSystem.py
    ├── test_NotificationSystem.py
    └── test_Yolo.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest tests/`)
6. Commit your changes (`git commit -am 'Add some feature'`)
7. Push to the branch (`git push origin feature/your-feature`)
8. Create a Pull Request

### Development Setup

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests to ensure everything works:
```bash
python -m pytest tests/ -v
```

3. Make your changes and test thoroughly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions, please open an issue on GitHub.
