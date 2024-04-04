import logging
import asyncio
from threading import Thread
import websockets
import time
import threading


logger = logging.getLogger(__name__)


# async def websocket_server(websocket, path):
#     while True:
#         try:
#             message = await websocket.recv()
#             print(f"Received message: {message}")
#             await websocket.send(f"Received: {message}")
#         except websockets.exceptions.ConnectionClosed:
#             print("Connection closed")
#             break


# def run_websocket_server():
#     asyncio.set_event_loop(asyncio.new_event_loop())
#     start_server = websockets.serve(websocket_server, "localhost", 8765)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()


# if __name__ == "__main__":
#     websocket_thread = threading.Thread(target=run_websocket_server)
#     websocket_thread.start()

#     # Main thread can do other stuff while websocket server is running
#     print("Websocket server is running in a separate thread.")

#     # Example: wait for the websocket thread to finish
#     websocket_thread.join()

class WebSocketServer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.websocket_thread = None

    async def websocket_server(self, websocket, path):
        while True:
            try:
                message = await websocket.recv()
                print(f"Received message: {message}")
                await websocket.send(f"Received: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

    def run_websocket_server(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(self.websocket_server, "0.0.0.0", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def start_server(self):
        self.websocket_thread = threading.Thread(target=self.run_websocket_server)
        self.websocket_thread.start()
        print("Websocket server is running in a separate thread.")

    def stop_server(self):
        if self.websocket_thread and self.websocket_thread.is_alive():
            self.websocket_thread.join()


if __name__ == "__main__":
    websocket_server = WebSocketServer()
    websocket_server.start_server()
    # Main thread can do other stuff while websocket server is running
    time.sleep(10)  # Example: Let the server run for 10 seconds
    print("xin chao")
    while True:
        time.sleep(1)
        print("hello")
    # websocket_server.stop_server()
