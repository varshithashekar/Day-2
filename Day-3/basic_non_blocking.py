import asyncio

class DeviceActor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.queue = asyncio.Queue()

    async def handle_message(self):
        while True:
            message = await self.queue.get()
            print(f"Device {self.device_id} received: {message}")

    async def send_message(self, message):
        await self.queue.put(message)

class ActorManager:
    def __init__(self):
        self.actors = {}

    def add_actor(self, device_id):
        actor = DeviceActor(device_id)
        self.actors[device_id] = actor
        asyncio.create_task(actor.handle_message())

    async def send_message(self, device_id, message):
        if device_id in self.actors:
            await self.actors[device_id].send_message(message)
        else:
            print(f"Device {device_id} not found")

async def get_user_input(manager):
    while True:
        device_id = int(input("Enter device ID to send a message (0 to quit): "))
        if device_id == 0:
            break
        message = input("Enter the message to send: ")
        await manager.send_message(device_id, message)

async def main():
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

    await get_user_input(manager)

if __name__ == "__main__":
    asyncio.run(main())
