import pyautogui
import time
from PIL import ImageGrab, ImageOps
import numpy as np

# Detection box coordinates for the obstacle region (based on the orange box)
dino_region = (452, 707, 550, 825 )  # Top-left: (435, 707), Bottom-right: (538, 824)

# The target color to detect (medium-dark gray)
target_color = (83, 83, 83)

# Initial sleep time (controls bot speed)
initial_sleep_time = 0.05  # Start with a small delay of 50 milliseconds


# Function to capture the game screen and return the pixel values of the region
def capture_screen(region):
    image = ImageGrab.grab(bbox=region)
    return image


# Function to detect the target color in the screen region
def detect_color(image, color):
    # Get the pixel data from the image
    pixels = np.array(image)

    # Check if any pixel in the image matches the target color (ignoring alpha channel if present)
    for row in pixels:
        for pixel in row:
            if tuple(pixel[:3]) == color:  # Compare only RGB, ignore alpha if any
                return True
    return False


# Function to handle jumping based on color detection with increasing speed
def start_jumping():
    time.sleep(5)  # Wait 5 seconds to allow the user to switch to the game window

    # Track the total time the bot has been running
    start_time = time.time()
    sleep_time = initial_sleep_time  # Start with the initial sleep time

    while True:
        # Capture the current state of the screen region
        screen_image = capture_screen(dino_region)

        # Check if the target color is detected in the image
        if detect_color(screen_image, target_color):
            pyautogui.press('space')  # Jump if the target color is detected
            time.sleep(0.1)  # Prevent multiple jumps by pausing briefly

        # Check how long the game has been running
        elapsed_time = time.time() - start_time

        # Every 10 seconds, increase the speed by 4% (reduce the sleep time)
        if elapsed_time >= 10:
            sleep_time *= 0.96  # Reduce sleep time by 4%
            start_time = time.time()  # Reset the start time for the next 10-second interval

        # Small delay, adjusted for game speed
        time.sleep(sleep_time)


# Start the function
start_jumping()
