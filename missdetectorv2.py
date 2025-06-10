#missdetectorv2
import cv2
import numpy as np
import mss
import time
import os
import random

#monitor region display on screen cv2.imshow('Image', image)

# Path to the Pico's mounted filesystem (adjust this if needed)
PICO_DRIVE = "G:/"
TRIGGER_FILE = os.path.join(PICO_DRIVE, "trigger.txt")

# Screen region above character
monitor_region = {"top": 545, "left": 850, "width": 250, "height": 130}

# HSV range for purple "MISS" text (adjust these values based on your screen/game settings)
lower_purple = np.array([125, 60, 60])
upper_purple = np.array([155, 255, 255])

print("Monitoring for MISS text...")

# Track the last written state to avoid redundant writes
last_written_state = None

def write_trigger(state):
    """
    Writes a trigger state (0 or 1) to the Pico's trigger.txt file, only if the state has changed.
    """
    global last_written_state

    # Check if the state has changed
    if state == last_written_state:
        return

    try:
        with open(TRIGGER_FILE, "w") as f:
            f.write(str(state))
        last_written_state = state  # Update the last written state
        print(f"✅ Wrote trigger state: {state}")
    except Exception as e:
        print(f"❌ Failed to write trigger state: {e}")

with mss.mss() as sct:
    while True:
        screenshot = sct.grab(monitor_region)
        img = np.array(screenshot)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_purple, upper_purple)
        purple_pixels = cv2.countNonZero(mask)

        # Detect if enough purple pixels are found (adjust this threshold based on your testing)
        if purple_pixels > 3700:
            print("✅ MISS detected - triggering bite! and waiting 5s.")
            write_trigger(1)  # Write '1' to trigger.txt
            time.sleep(3)
        else:
            write_trigger(0)  # Write '0' to trigger.txt (only if needed)

        # Run loop at 3 times per second
        time.sleep(random.uniform(0.25, 0.3))

        if cv2.waitKey(1) == 27:
            print("Exiting...")
            break
