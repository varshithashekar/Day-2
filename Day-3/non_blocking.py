import threading
import queue
import time

class DeviceActor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self.handle_message)
        self.thread.start()

    def handle_message(self):
        while self.running:
            try:
                message = self.queue.get(timeout=1)  # Adjust timeout as needed
                print(f"Device {self.device_id} received: {message}")
            except queue.Empty:
                continue

    def send_message(self, message):
        self.queue.put(message)

    def stop(self):
        self.running = False
        self.thread.join()

class ActorManager:
    def __init__(self):
        self.actors = {}

    def add_actor(self, device_id):
        actor = DeviceActor(device_id)
        self.actors[device_id] = actor

    def send_message(self, device_id, message):
        if device_id in self.actors:
            self.actors[device_id].send_message(message)
        else:
            print(f"Device {device_id} not found")

    def stop_all(self):
        for actor in self.actors.values():
            actor.stop()

def get_user_input(manager):
    while True:
        device_id = int(input("Enter device ID to send a message (0 to quit): "))
        if device_id == 0:
            break
        message = input("Enter the message to send: ")
        manager.send_message(device_id, message)

def main():
    manager = ActorManager()
    while True:
        try:
            num_actors = int(input("Enter the number of devices to initialize: "))
            if num_actors <= 0:
                print("Please enter a positive number.")
                continue
            for device_id in range(1, num_actors + 1):
                manager.add_actor(device_id)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    get_user_input(manager)
    manager.stop_all()

if __name__ == "__main__":
    main()
