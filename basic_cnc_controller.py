import serial
import time
import re
import sys
import toml

class BasicCNCController:
    def __init__(self, config):
        self.config = config
        print(f"Initializing controller on port {self.config['ports']['controller']}")
        self.ser = serial.Serial(
            self.config['ports']['controller'],
            self.config['serial']['baudrate'],
            timeout=self.config['serial']['timeout']
        )
        self.position = {"X": 0, "Y": 0, "Z": 0}
        self.is_running = True

    def run(self):
        print(f"Basic CNC Controller running on {self.ser.port}")
        sys.stdout.flush()
        while self.is_running:
            if self.ser.in_waiting:
                command = self.ser.readline().decode("utf-8").strip()
                print(f"Received command: {command}")
                sys.stdout.flush()
                response = self.process_command(command)
                print(f"Sending response: {response.strip()}")
                sys.stdout.flush()
                self.ser.write(response.encode("utf-8"))
                self.ser.flush()
            time.sleep(self.config['controller']['update_interval'])

    def process_command(self, command):
        if command.startswith("G0") or command.startswith("G1"):  
            match = re.findall(r"([XYZ])(-?\d+(\.\d+)?)", command)
            for axis, value, _ in match:
                self.position[axis] = float(value)
            return f"OK - Moved to X{self.position['X']} Y{self.position['Y']} Z{self.position['Z']}\n"
        elif command == "M114":  
            return f"X:{self.position['X']} Y:{self.position['Y']} Z:{self.position['Z']}\n"
        elif command == "M0":  
            self.is_running = False
            return "OK - Stopping\n"
        else:
            return "Unknown command\n"

if __name__ == "__main__":
    with open("cnc_config.toml", "r") as config_file:
        config = toml.load(config_file)
    controller = BasicCNCController(config)
    controller.run()
