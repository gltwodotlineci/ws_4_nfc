import asyncio
from websockets.asyncio.server import serve
from smartcard.System import readers
from smartcard.util import toHexString
import json
import requests

# Avoiding SSL warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Get available NFC readers
available_readers = readers()
if not available_readers:
    raise Exception("No NFC reader detected!")

reader = available_readers[0]  # Use the first available reader

def read_card():
    """
    Reads an NFC card UID using pyscard.
    """
    tag_id = ''
    tag_id_good = False

    while not tag_id_good:
        try:
            connection = reader.createConnection()
            connection.connect()

            # APDU command to get UID (ACR122-specific)
            get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(get_uid)

            # Status Word 0x90 0x00 means success
            if sw1 == 0x90 and sw2 == 0x00:
                tag_id = ''.join(format(x, '02X') for x in response)
        except Exception as e:
            print("Error reading card:", e)
            tag_id = ''

        if tag_id:
            tag_id_good = True
            return tag_id

async def hello(websocket):
    """
    WebSocket handler for receiving commands and responding with NFC tag ID.
    """
    print("Enterging to async")
    msg = await websocket.recv()

    async for message in websocket:
        print(f"Received: {message}")


        if msg == "reed_tag_id":
            tag_id = read_card()
            print(f"tag_id <=> {tag_id}")

            resp = requests.post(
                'http://localhost:57347/api/card/scan/',
                data={'tag_id': tag_id},
                verify=False
            )

            if resp.status_code != 200:
                json_retour = json.dumps({'message': 'NotFound', 'tag_id': ''})
            else:
                json_retour = json.dumps(resp.json())

            print("Response: ", json_retour)
            await websocket.send(json_retour)


async def main():
    async with serve(hello, "localhost", 8001):
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
