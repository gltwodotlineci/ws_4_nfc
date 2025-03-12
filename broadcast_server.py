import asyncio
import websockets
import json

# Avoiding SSL warning
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# List to store connected clients
clients = set()

# Broadcasting function
async def broadcast(message):
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected, removing from list")
            disconnected_clients.add(client)
    
    # Remove disconnected clients
    clients.difference_update(disconnected_clients)

# WS server handler
async def handler(websocket):
    clients.add(websocket)
    print("Client connected")

    try:
        async for data in websocket:
            # Receing data from client
            received_data = json.loads(data)
            print(f"Received message: {received_data['message']}")

            # Broadcasting received data message
            if received_data.get('message') == "Bill":
                message = {'bill': received_data['bill'], 'received_bill': "Bill recived"}
                await broadcast(json.dumps(message))

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Removing client when disconnected
        clients.discard(websocket)
        print("Client disconnected")

# Start WS server
async def main():
    server = await websockets.serve(handler, "127.0.0.1", 8003)
    print("WebSocket Server running on ws://127.0.0.2:8003")
    await server.wait_closed()

# Run the Wb server
if __name__ == "__main__":
    asyncio.run(main())
