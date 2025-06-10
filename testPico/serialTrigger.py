import serial
import time
import sys

# --- Configuration ---
# IMPORTANT: You NEED to change 'COM3' to the actual serial port your Pico uses.
# On Windows, this will be 'COMx' (e.g., 'COM3', 'COM4').
# On Linux/macOS, this will be something like '/dev/ttyACM0' or '/dev/ttyUSB0'.
# You can find the correct port in your operating system's Device Manager (Windows)
# or by checking `ls /dev/tty*` (Linux/macOS) when the Pico is plugged in.
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200 # This baud rate is common and generally reliable.

def send_trigger_to_pico(ser_conn):
    """Sends a 'TRIGGER' command over the serial connection."""
    try:
        command = "TRIGGER\n" # The '\n' is a newline character, signaling end of command
        ser_conn.write(command.encode('utf-8')) # Encode the string to bytes
        print(f"Sent: '{command.strip()}' to Pico.")
    except serial.SerialException as e:
        print(f"Error sending data: {e}. Is the Pico connected and listening?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """Main function to handle user interaction and serial communication."""
    ser = None # Initialize serial connection variable

    try:
        # Attempt to open the serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Successfully opened serial port {SERIAL_PORT} at {BAUD_RATE} baud.")
        print("Waiting for Pico to be ready...")
        time.sleep(2) # Give the Pico a moment to initialize after connection

        while True:
            user_input = input("\nSend 'TRIGGER' to Pico? (y/n, or 'q' to quit): ").lower().strip()

            if user_input == 'y':
                send_trigger_to_pico(ser)
            elif user_input == 'n':
                print("No trigger sent.")
            elif user_input == 'q':
                print("Exiting PC detector script.")
                break
            else:
                print("Invalid input. Please enter 'y', 'n', or 'q'.")

    except serial.SerialException as e:
        print(f"Could not open serial port {SERIAL_PORT}: {e}")
        print("Please ensure:")
        print("1. The Pico is connected.")
        print(f"2. The port '{SERIAL_PORT}' is correct (check Device Manager/ls /dev/tty*).")
        print("3. No other program is using the port.")
    except KeyboardInterrupt:
        print("\nScript interrupted by user (Ctrl+C). Exiting.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")
        print("PC Detector script finished.")

if __name__ == "__main__":
    # Make sure you have pyserial installed: pip install pyserial
    main()
