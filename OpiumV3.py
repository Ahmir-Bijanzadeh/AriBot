import time
import random
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import usb_hid

# Initialize USB HID Keyboard
keyboard = Keyboard(usb_hid.devices)

# Path to the trigger.txt file on the CIRCUITPY drive
TRIGGER_FILE = "/trigger.txt"

# Track currently pressed keys
pressed_keys = set()

# Shadow Bite cooldown tracking
last_bite_time = 0  # Initialize to 0 to allow the first press
bite_cooldown = 8.75  # Cooldown time in seconds
last_move_time = time.monotonic()
last_known_trigger_state = 0

def read_trigger():
    global last_known_trigger_state
    try:
        with open(TRIGGER_FILE, "r") as f:
            state = f.read().strip()
            if state in ["0", "1"]:
                last_known_trigger_state = int(state)
                return last_known_trigger_state
            return 0
    except OSError as e:
        print(f"[Warning] Error reading trigger.txt: {e} assuming opposite state")
        # Flip the last known trigger state, or just return the opposite
        last_known_trigger_state = 1 - last_known_trigger_state
        return last_known_trigger_state

# Utilities for HID key management
def hold_key(keycode):
    if keycode not in pressed_keys:
        keyboard.press(keycode)
        pressed_keys.add(keycode)

def release_key(keycode):
    if keycode in pressed_keys:
        keyboard.release(keycode)
        pressed_keys.remove(keycode)

def tap_key(keycode, duration=None):
    if duration is None:
        duration = random.uniform(0.07, 0.22)  # Default duration for key press
    hold_key(keycode)
    time.sleep(duration)
    release_key(keycode)
    time.sleep(0.05)  # Add a small delay after releasing the key

# Movement Actions
def quint_jump():
    print("[Action] Quintuple Jump")
    tap_key(Keycode.Z, random.uniform(0.08, 0.11))
    time.sleep(random.uniform(0.08, 0.14))
    tap_key(Keycode.Z, random.uniform(0.08, 0.11))
    time.sleep(random.uniform(0.08, 0.14))
    tap_key(Keycode.C, random.uniform(0.09, 0.13))
    time.sleep(random.uniform(0.08, 0.14))

def drop_down():
    print("[Action] Drop DOWN")
    hold_key(Keycode.DOWN_ARROW)
    time.sleep(random.uniform(0.09, 0.22))
    tap_key(Keycode.Z)
    time.sleep(random.uniform(0.05, 0.12))
    tap_key(Keycode.C)
    time.sleep(random.uniform(0.05, 0.12))
    release_key(Keycode.DOWN_ARROW)

def flashjump_up():
    print("[Action] Flashjump UP")
    hold_key(Keycode.UP_ARROW)
    time.sleep(random.uniform(0.09, 0.22))
    tap_key(Keycode.Z)
    time.sleep(random.uniform(0.03, 0.12))
    tap_key(Keycode.Z)
    time.sleep(random.uniform(0.05, 0.12))
    release_key(Keycode.UP_ARROW)
    time.sleep(random.uniform(0.33, 0.44))
    tap_key(Keycode.C)

# Looting Action
def loot():
    global last_move_time
    print("\n=== LOOTING START ===")
    tap_key(Keycode.H)
    time.sleep(random.uniform(0.6, 0.9))
    quint_jump()
    time.sleep(random.uniform(1.6, 2.1))
    tap_key(Keycode.RIGHT_ARROW)
    time.sleep(random.uniform(0.14, 0.28))
    quint_jump()
    time.sleep(random.uniform(0.28, 0.44))
    quint_jump()
    time.sleep(random.uniform(0.77, 1.21))
    quint_jump()
    time.sleep(random.uniform(0.77, 1.15))
    tap_key(Keycode.L)
    time.sleep(random.uniform(0.77, 1.10))
    tap_key(Keycode.LEFT_ARROW)
    time.sleep(random.uniform(0.28, 0.44))
    tap_key(Keycode.H)
    time.sleep(random.uniform(0.39, 0.70))
    print("=== LOOTING END ===\n")

# Main Farming Loopv
def main_farming_loop():
    global last_bite_time  # Use the global variable to track cooldown
    last_loot_time = time.monotonic()
    last_move_time = time.monotonic()
    last_buff_time = 200

    print("Starting MISS-trigger-only Shadow Bite farming...")

    try:
        while True:
            # Check for MISS trigger
            trigger_state = read_trigger()
            now = time.monotonic()  # Get the current time in seconds

            if trigger_state == 1:
                # Check if enough time has passed since the last Shadow Bite
                if now - last_bite_time >= bite_cooldown:
                    print("[MISS] Shadow Bite Triggered")
                    time.sleep(random.uniform(0.15, 0.30))  # Small random delay before pressing V
                    tap_key(Keycode.V,random.uniform(0.8, 1.2))  # Press Shadow Bite
                    last_bite_time = now  # Update the time of the last Shadow Bite
                elif bite_cooldown - (now - last_bite_time) >= 3 and bite_cooldown - (now - last_bite_time) <= 6:
                    tap_key(Keycode.Z)
                    time.sleep(random.uniform(0.06, 0.14))
                    tap_key(Keycode.C)
                    time.sleep(random.uniform(0.3, 0.4))
                    tap_key(Keycode.Z)
                    time.sleep(random.uniform(0.06, 0.14))
                    tap_key(Keycode.C)
                    time.sleep(random.uniform(0.3, 0.4))
                    tap_key(Keycode.C)
                else:
                    remaining_cd = bite_cooldown - (now - last_bite_time)
                    print(f"[MISS] Shadow Bite on cooldown: {remaining_cd:.2f}s remaining")

            # Add a small delay between loop iterations to avoid spamming
            time.sleep(random.uniform(0.33, 0.50))

            # Movement and looting logic
            time_since_loot = now - last_loot_time
            time_since_moved = now - last_move_time
            time_since_buffed = now - last_buff_time

            # Buffing with spears
            if time_since_buffed >= random.uniform(178, 189):
                print(f"Buffing (time since buff: {time_since_buffed:.2f})")
                time.sleep(random.uniform(0.20, 0.39))
                tap_key(Keycode.TWO)
                last_buff_time = time.monotonic()

            # Perform movement if idle for too long
            if time_since_moved >= random.uniform(25, 44):
                print(f"[Idle] Moving (time since move: {time_since_moved:.2f})")
                time.sleep(random.uniform(0.20, 0.39))
                drop_down()
                time.sleep(random.uniform(0.77, 1.10))
                flashjump_up()
                time.sleep(random.uniform(0.20, 0.39))
                last_move_time = time.monotonic()
            
            # Perform looting if idle for too long
            if time_since_loot >= random.uniform(54, 61):
                print(f"[Idle] Looting (time since loot: {time_since_loot:.2f})")
                time.sleep(random.uniform(0.20, 0.39))
                loot()
                last_loot_time = time.monotonic()
                last_move_time = time.monotonic()

            # Random inventory interaction
            if random.random() < 0.0001:
                print("[Interaction] Random Inventory Open")
                tap_key(Keycode.I)
                time.sleep(random.uniform(0.5, 1.5))

    except KeyboardInterrupt:
        print("\n[Program Stopped by User]")
        # Release all keys to ensure no stuck keys
        for key in pressed_keys.copy():
            release_key(key)

# Start the script
if __name__ == "__main__":
    startup_delay = 3
    print(f"Starting in {startup_delay:.2f} seconds...")
    time.sleep(startup_delay)
    main_farming_loop()