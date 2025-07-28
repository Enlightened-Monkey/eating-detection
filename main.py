#!/usr/bin/env python3
import sys
import os
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './src')))

from cmd_app import CMDApp
from food_detection_system import FoodDetectionSystem
from notification_system import NotificationSystem

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

# Load or create settings file
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "objects_to_detect": ["bottle"],
            "threshold": 0.5,
            "camera_settings": {
                "resolution": [640, 480],
                "frame_check_interval": 1
            },
            "user_ids": [1]
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(default_settings, f, indent=4)
        return default_settings
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def notification_callback(message):
    print(f"NOTIFICATION: {message}")

def detection_loop(food_system, user_settings, running_flag):
    while running_flag['running']:
        detected = food_system.check_detections()
        if detected:
            print(f"Detected: {detected}")
        time.sleep(user_settings['camera_settings']['frame_check_interval'])

def settings_input_loop(user_settings):
    print("You can change settings by typing e.g. 'threshold 0.7' or 'frame_check_interval 2'. Type 'exit' to finish.")
    while True:
        inp = input("Setting: ")
        if inp.strip().lower() == "exit":
            break
        try:
            key, value = inp.split()
            if key == "threshold":
                user_settings["threshold"] = float(value)
                print(f"Threshold set to {user_settings['threshold']}")
            elif key == "frame_check_interval":
                user_settings["camera_settings"]["frame_check_interval"] = float(value)
                print(f"Frame check interval set to {user_settings['camera_settings']['frame_check_interval']}")
            elif key == "resolution":
                width, height = map(int, value.split('x'))
                user_settings["camera_settings"]["resolution"] = [width, height]
                print(f"Resolution set to {user_settings['camera_settings']['resolution']}")
            else:
                print("Unknown setting.")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    user_settings = load_settings()
    cmd_app = CMDApp(user_settings)
    notification_system = NotificationSystem()

    # Subscribe user to notifications
    notification_system.subscribe(1, notification_callback)

    food_system = FoodDetectionSystem(user_settings, notification_system)
    running_flag = {'running': False}

    while True:
        command = input("Enter command (type 'help' for options): ").strip()
        try:
            if command == "exit":
                print("Exiting application.")
                running_flag['running'] = False
                food_system.release_camera()
                break
            elif command in ["help", "what_to_detect", "threshold", "camera_settings"]:
                cmd_app.run_command(command)
                save_settings(user_settings)
            elif command == "start":
                if not running_flag['running']:
                    print("Starting detection...")
                    running_flag['running'] = True
                    food_system.start_detection(running_flag)
                else:
                    print("Detection is already running.")
            elif command == "stop":
                if running_flag['running']:
                    print("Stopping detection...")
                    running_flag['running'] = False
                else:
                    print("Detection is not running.")
            else:
                print("Unknown command. Type 'help' to see available commands.")
        except Exception as e:
            print(f"Error: {str(e)}")

    # End detection after exiting the loop
    running_flag['running'] = False
    food_system.release_camera()

if __name__ == "__main__":
    main()