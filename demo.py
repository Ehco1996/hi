import sys
import asyncio
import socket
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        print("Data received: {!r}".format(data))
        asyncio.create_task(self.send_back(data))

    async def send_back(self, data):
        message = data.decode()
        print("Send: {!r}".format(message))
        self.transport.write(data)

        await asyncio.sleep(10)
        print("Close the client socket")
        self.transport.close()


async def start_async_server():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(lambda: EchoServerProtocol(), HOST, PORT)
    print(f"start async server at: {HOST}:{PORT}")
    async with server:
        await server.serve_forever()


def start_sync_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"start sync server at: {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            time.sleep(0.1)
            with conn:
                print("Connected by", addr)
                data = conn.recv(1024)
                time.sleep(10)
                conn.sendall(data)


def say_hi():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

    print("Received", repr(data))


if __name__ == "__main__":
    if "async" in sys.argv:
        asyncio.run(start_async_server())
    else:
        start_sync_server()
