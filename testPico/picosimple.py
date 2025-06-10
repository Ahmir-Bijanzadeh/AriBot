# pico_keyboard_script.py
# This script runs on a Raspberry Pi Pico with CircuitPython installed.
# It emulates a USB keyboard and listens for serial commands from a connected PC.

import time
import sys # Used for reading serial input
import usb_hid # Core module for USB Human Interface Device (HID)
from adafruit_hid.keyboard import Keyboard # Class to emulate a keyboard
from adafruit_hid.keycode import Keycode # Contains key definitions (e.g., Keycode.F)

# --- Configuration ---
# Set up the keyboard emulation
# usb_hid.devices usually contains a list of available HID interfaces.
# We pass this list to the Keyboard class to tell it which interface to use.
keyboard = Keyboard(usb_hid.devices)

print("Pico Keyboard Script: Initialized.")
print("Waiting for serial commands from PC...")

def type_string(text_to_type):
    """
    Types a given string using the emulated USB keyboard.
    Each character is sent individually.
    """
    for char in text_to_type:
        if char.isalpha(): # Check if it's an alphabet character
            # Convert character to its corresponding Keycode (e.g., 'f' to Keycode.F)
            # Make sure it's uppercase for Keycode mapping.
            keycode = getattr(Keycode, char.upper())
            keyboard.press(keycode) # Press the key
            time.sleep(0.05) # Small delay for key press
            keyboard.release_all() # Release all pressed keys (important!)
        else:
            # Handle non-alphabetic characters if needed (e.g., numbers, symbols)
            # For now, just print a warning for simplicity.
            print(f"Warning: Cannot type non-alphabetic character '{char}'.")
        time.sleep(0.05) # Small delay between characters for better reliability

def process_command(command):
    """
    Processes a received command from the serial port.
    """
    if command == "TRIGGER":
        print("Pico: Received 'TRIGGER' command. Typing 'finished'...")
        type_string("finished")
        print("Pico: Finished typing.")
    else:
        print(f"Pico: Unknown command received: '{command}'")

# Main loop: Continuously check for serial input
while True:
    # sys.stdin.buffered().peek() checks if there's any data in the buffer
    # without removing it. This prevents blocking if no data is present.
    if sys.stdin.buffered().peek():
        # Read a line from the serial input (from the PC)
        # .readline() reads until a newline character ('\n')
        # .strip() removes leading/trailing whitespace, including the newline
        received_command = sys.stdin.readline().strip()
        process_command(received_command)
    time.sleep(0.01) # Small delay to prevent busy-waiting and allow other tasks
