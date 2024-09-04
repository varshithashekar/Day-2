import serial
import device_pb2
from google.protobuf.message import DecodeError

class SerialDeviceEmulator:
    def __init__(self, port, baudrate=9600):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.device_id = "Device123"  

    def listen(self):
        while True:
            if self.serial_port.in_waiting:
                data = self.serial_port.read_until(b'\n')
                self.handle_request(data)

    def handle_request(self, data):
        try:
            request = device_pb2.CommandRequest()
            request.ParseFromString(data)

            response = device_pb2.CommandResponse()
            response.device_id = self.device_id


            if request.command == device_pb2.CommandType.STATUS:
                response.status = device_pb2.ResponseType.OK
                response.message = "Device is online."

            elif request.command == device_pb2.CommandType.START:
                response.status = device_pb2.ResponseType.OK
                response.message = "Device started."

            elif request.command == device_pb2.CommandType.STOP:
                response.status = device_pb2.ResponseType.OK
                response.message = "Device stopped."

            else:
                response.status = device_pb2.ResponseType.ERROR
                response.message = "Unknown command."

            # Send response
            self.serial_port.write(response.SerializeToString() + b'\n')

        except DecodeError:
            print("Failed to decode protobuf message.")

    def close(self):
        self.serial_port.close()

if __name__ == "__main__":
    emulator = SerialDeviceEmulator('COM3')
    try:
        emulator.listen()
    except KeyboardInterrupt:
        emulator.close()
