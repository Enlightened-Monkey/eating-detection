class CMDApp:
    def __init__(self, user_settings):
        self.user_settings = user_settings
        self.commands = {
            'help': self.display_help,
            'start': None,  # handled in main.py
            'stop': None,   # handled in main.py
            'what_to_detect': self.set_detection_targets,
            'threshold': self.set_threshold,
            'camera_settings': self.set_camera_settings
        }

    def display_help(self):
        help_text = """
        Available commands:
        - help: Display this help message
        - start: Start the food detection process
        - stop: Stop the food detection process
        - what_to_detect: Specify food items to detect (default: bottle)
        - threshold: Set the detection confidence threshold (0.0-1.0)
        - camera_settings: Configure camera resolution and frame check interval
        - exit: Exit the application
        """
        print(help_text)

    def set_detection_targets(self):
        targets = input("Enter objects to detect, separated by commas (e.g. apple,banana): ").strip()
        if not targets:
            raise ValueError("No detection targets provided.")
        self.user_settings['objects_to_detect'] = [t.strip() for t in targets.split(',')]
        print(f"Detection targets set to: {self.user_settings['objects_to_detect']}")

    def set_threshold(self):
        threshold = input("Enter detection threshold (0.0-1.0, e.g. 0.5): ")
        try:
            threshold = float(threshold)
            if not 0.0 <= threshold <= 1.0:
                raise ValueError("Threshold must be between 0.0 and 1.0.")
            self.user_settings['threshold'] = threshold
            print(f"Detection threshold set to: {self.user_settings['threshold']}")
        except ValueError as e:
            raise ValueError(f"Invalid threshold value: {str(e)}")

    def set_camera_settings(self):
        resolution = input("Enter resolution (e.g. 640x480): ")
        interval = input("Enter frame check interval (seconds, e.g. 1): ")
        try:
            width, height = map(int, resolution.split('x'))
            if width <= 0 or height <= 0:
                raise ValueError("Resolution dimensions must be positive.")
            interval = float(interval)
            if interval <= 0:
                raise ValueError("Frame check interval must be positive.")
            self.user_settings['camera_settings']['resolution'] = [width, height]
            self.user_settings['camera_settings']['frame_check_interval'] = interval
            print(f"Camera settings updated: {self.user_settings['camera_settings']}")
        except ValueError as e:
            raise ValueError(f"Invalid camera settings: {str(e)}")

    def run_command(self, command):
        if command in self.commands and self.commands[command]:
            self.commands[command]()
        else:
            print("Unknown command or handled outside CMDApp.")