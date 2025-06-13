from dotenv import load_dotenv
import asyncio
import websockets
import json, os

# Token for identification
load_dotenv()
token_key = os.getenv("DEVICE_TOKEN_KEY")

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
                # Send bill amount message as json
                message = {'bill': received_data['bill'],
                           'token_key':token_key, 'received_bill': "Bill recived"}
                print(message.get('token_id'))
                await broadcast(json.dumps(message))

    except Exception as e:
        print(f"Error occurred: {e}")


async def main():
    server = await websockets.serve(handler, "127.0.0.1", 8010)
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
