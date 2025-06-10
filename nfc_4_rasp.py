import asyncio, websockets
from smartcard.System import readers
import json
import requests

# Avoiding SSL warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

token_key = "21204489f766b2c3373f19051f132464235c5ec883e5c0d49b4e3b17d683bf04"

headers = {
    'Authorization': f'Bearer {token_key}'
}
# Get available NFC readers
available_readers = readers()
if not available_readers:
    raise Exception("No NFC reader detected!")

reader = available_readers[0]  # Use the first available reader

def read_card()-> str:
    """
    Reads an NFC card UID using pyscard.
    :tag_id: str
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

  # When it recive the message to reed the card
    if msg == "reed_tag_id":
        tag_id = read_card()
        print(f"tag_id <=> {tag_id}")

        resp = requests.post(
        'http://glencho.casacam.net:57347/api/card/scan/',
        data={'tag_id': tag_id},
        headers=headers,
        verify=False
        )

        # The case the card does not exist on kiosk DB
        if resp.status_code != 200:
            json_retour = json.dumps({'message': 'NotFound', 'tag_id': ''})
        # Sending the tag_id as json data
        else:
            json_retour = json.dumps(resp.json())

        print("Response: ", json_retour)
        await websocket.send(json_retour)


async def main():
  async with websockets.serve(hello, "127.0.0.1", 8002):
    await asyncio.Future() 


if __name__ == "__main__":
    asyncio.run(main())
