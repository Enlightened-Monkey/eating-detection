# Eating Detection

This project detects selected objects (e.g., bottles) in camera images, notify user when certain object is detected and provides a command-line interface for configuration and control.

## Step-by-step instructions

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
python src/notification_client.py
```

### 5. Run the main application

In another terminal, start the main program:

```bash
python src/main.py
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

Settings are saved in `src/settings.json`. You can edit this file manually or use the CLI commands.

For more information, see the source code
