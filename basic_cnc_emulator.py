import serial
import time
import sys
import toml

def send_command(ser, command, delay):
    print(f"Sending: {command}")
    sys.stdout.flush()
    ser.write(f"{command}\n".encode("utf-8"))
    ser.flush()
    time.sleep(delay)
    response = ser.read(ser.in_waiting).decode("utf-8")
    print(f"Received: {response.strip()}")
    sys.stdout.flush()
    return response

if __name__ == "__main__":
    with open("cnc_config.toml", "r") as config_file:
        config = toml.load(config_file)
    
    print(f"Starting basic emulator with port {config['ports']['emulator']}")
    sys.stdout.flush()
    try:
        ser = serial.Serial(
            config['ports']['emulator'],
            config['serial']['baudrate'],
            timeout=config['serial']['timeout']
        )
        print(f"Serial port {config['ports']['emulator']} opened successfully")
        sys.stdout.flush()
        
        send_command(ser, "G0 X10 Y20 Z5", config['emulator']['command_delay'])
        send_command(ser, "M114", config['emulator']['command_delay'])
        send_command(ser, "G1 X15 Y25 Z10", config['emulator']['command_delay'])
        send_command(ser, "M114", config['emulator']['command_delay'])
        send_command(ser, "M0", config['emulator']['command_delay'])
        
        ser.close()
        print("Emulation completed successfully")
        sys.stdout.flush()
    except serial.SerialException as e:
        print(f"Error opening serial port {config['ports']['emulator']}: {e}")
        sys.stdout.flush()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.stdout.flush()
