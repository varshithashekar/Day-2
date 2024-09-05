import dearpygui.dearpygui as dpg
import random
import time

class IoTDeviceEmulator:
    def __init__(self):
        self.device_status = "Disconnected"
        self.device_data = {}

    def connect(self, device_name):
        self.device_status = f"Connected to {device_name}"
        time.sleep(1)  
        print(self.device_status)

    def send_command(self, command):
        if command == "read_sensor":
            self.device_data["sensor_value"] = round(random.uniform(0, 100), 1)
            response = f"Sensor value: {self.device_data['sensor_value']}"
        else:
            response = "Unknown command"
        print(response)
        return response

    def get_status(self):
        return self.device_status

emulator = IoTDeviceEmulator()

def execute_command(sender, app_data, user_data):
    command = dpg.get_value("command_input")
    if command.startswith("connect"):
        _, device_name = command.split(" ", 1)
        emulator.connect(device_name)
    elif command.startswith("send"):
        _, command_text = command.split(" ", 1)
        response = emulator.send_command(command_text)
        dpg.set_value("response_text", response)
    elif command == "status":
        status = emulator.get_status()
        dpg.set_value("response_text", status)
    else:
        dpg.set_value("response_text", "Unknown command. Please use 'connect <device>', 'send <command>', or 'status'.")

def main():
    dpg.create_context()

    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: dpg.stop_dearpygui())

    with dpg.window(label="IoT Command Interface", width=600, height=400):
        dpg.add_input_text(label="Enter Command", tag="command_input")
        dpg.add_button(label="Submit Command", callback=execute_command)
        dpg.add_text("", tag="response_text")  # Text widget to show command responses

    dpg.create_viewport(title='IoT Command Interface', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
