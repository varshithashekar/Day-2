from __future__ import annotations
import asyncio
import contextlib
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from typing import Optional, AsyncGenerator, Union
from typing_extensions import Literal
from serial import Serial, serial_for_url

TimeoutProperties = Union[Literal["write_timeout"], Literal["timeout"]]

class AsyncSerial:
    @classmethod
    async def create(
        cls,
        port: str,
        baud_rate: int,
        timeout: Optional[float] = None,
        write_timeout: Optional[float] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        reset_buffer_before_write: bool = False,
    ) -> AsyncSerial:
        loop = loop or asyncio.get_running_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        serial = await loop.run_in_executor(
            executor=executor,
            func=partial(
                serial_for_url,
                url=port,
                baudrate=baud_rate,
                timeout=timeout,
                write_timeout=write_timeout
            ),
        )
        return cls(
            serial=serial,
            executor=executor,
            loop=loop,
            reset_buffer_before_write=reset_buffer_before_write,
        )

    def __init__(
        self,
        serial: Serial,
        executor: ThreadPoolExecutor,
        loop: asyncio.AbstractEventLoop,
        reset_buffer_before_write: bool,
    ) -> None:
        self._serial = serial
        self._executor = executor
        self._loop = loop
        self._reset_buffer_before_write = reset_buffer_before_write 
    
    async def read_until(self, match: bytes) -> bytes:
        return await self._loop.run_in_executor(
            executor=self._executor,
            func=partial(self._serial.read_until, expected=match),
        )

    async def write(self, data: bytes) -> None:
        await self._loop.run_in_executor(
            executor=self._executor,
            func=lambda: self._sync_write(data=data),
        )

    def _sync_write(self, data: bytes) -> None:
        if self._reset_buffer_before_write:
            self._serial.reset_input_buffer()
        self._serial.write(data=data)
        self._serial.flush()

    async def open(self) -> None:
        if not self._serial.is_open:
            return await self._loop.run_in_executor(
                executor=self._executor, func=self._serial.open
            )
    
    async def close(self) -> None:
        if self._serial.is_open:
            return await self._loop.run_in_executor(
                executor=self._executor, func=self._serial.close
            )
    
    async def is_open(self) -> bool:
        return self._serial.is_open is True
    
    def reset_input_buffer(self) -> None:
        self._serial.reset_input_buffer()

    @contextlib.asynccontextmanager
    async def timeout_override(
        self, timeout_property: TimeoutProperties, timeout: Optional[float]
    ) -> AsyncGenerator[None, None]:
        default_timeout = getattr(self._serial, timeout_property)
        override = timeout is not None and default_timeout != timeout
        try:
            if override:
                await self._loop.run_in_executor(
                    executor=self._executor,
                    func=lambda: setattr(self._serial, timeout_property, timeout),
                )
            yield
        finally:
            if override:
                await self._loop.run_in_executor(
                    executor=self._executor,
                    func=lambda: setattr(
                        self._serial, timeout_property, default_timeout
                    ),
                )


import asyncio
import threading
from async_serial import AsyncSerial

async def writer_task(port: str, baud_rate: int, messages: list):
    print(f"Writer task starting on port {port}")
    write_serial = await AsyncSerial.create(
        port=port,
        baud_rate=baud_rate,
        timeout=1.0,
        write_timeout=1.0,
        reset_buffer_before_write=True
    )

    await write_serial.open()
    print(f"Writer connection opened on {port}")

    try:
        for msg in messages:
            print(f"Writing message: {msg.decode().strip()}")
            async with write_serial.timeout_override("write_timeout", 0.5):
                await write_serial.write(msg)
            print(f"Message written with 0.5s timeout override")
            await asyncio.sleep(1)  # Wait a bit between messages
    finally:
        await write_serial.close()
        print(f"Writer connection closed on {port}")

async def reader_task(port: str, baud_rate: int):
    print(f"Reader task starting on port {port}")
    read_serial = await AsyncSerial.create(
        port=port,
        baud_rate=baud_rate,
        timeout=2.0,
        write_timeout=1.0,
        reset_buffer_before_write=True
    )

    await read_serial.open()
    print(f"Reader connection opened on {port}")

    try:
        while True:
            try:
                response = await read_serial.read_until(b"\n")
                print(f"Received: {response.decode().strip()}")
            except asyncio.TimeoutError:
                print("Read operation timed out, continuing...")
    finally:
        await read_serial.close()
        print(f"Reader connection closed on {port}")

def run_writer_in_thread(loop, writer_port, baud_rate, messages):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(writer_task(writer_port, baud_rate, messages))

async def main():
    writer_port = "/dev/pts/4"  # Replace with your actual write port
    reader_port = "/dev/pts/5"  # Replace with your actual read port
    baud_rate = 9600

    messages = [
        b"Hello from thread 1!\n",
        b"This is message 2.\n",
        b"And here's message 3.\n",
        b"Final message from thread!\n"
    ]

    # Create a new event loop for the writer thread
    writer_loop = asyncio.new_event_loop()

    # Start the writer task in a separate thread
    writer_thread = threading.Thread(
        target=run_writer_in_thread,
        args=(writer_loop, writer_port, baud_rate, messages)
    )
    writer_thread.start()

    # Start the reader task in the main thread
    reader = asyncio.create_task(reader_task(reader_port, baud_rate))

    # Let the tasks run for a while
    await asyncio.sleep(10)  # Adjust this time as needed

    # Cancel the reader task
    reader.cancel()
    try:
        await reader
    except asyncio.CancelledError:
        print("Reader task cancelled")

    # Wait for the writer thread to finish
    writer_thread.join()
    writer_loop.close()

if __name__ == "__main__":
    asyncio.run(main())

