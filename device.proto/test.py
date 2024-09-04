import serial
import device_pb2

ser = serial.Serial('COM3', 9600)

request = device_pb2.CommandRequest()
request.device_id = "Device123"
request.command = device_pb2.CommandType.STATUS

ser.write(request.SerializeToString() + b'\n')

response_data = ser.read_until(b'\n')
response = device_pb2.CommandResponse()
response.ParseFromString(response_data)

print(f"Response: {response.status}, Message: {response.message}")

ser.close()
