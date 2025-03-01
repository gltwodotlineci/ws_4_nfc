import asyncio
from websockets.asyncio.server import serve
from py122u import nfc
import json
import requests

# Avoiding ssl
from urllib3.exceptions import InsecureRequestWarning
# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

reader = nfc.Reader()

def read_card():
  tag_id = ''
  tag_id_good = False
  while tag_id_good == False:
    try:
      tag_id = ''
      reader.connect()
      for non_hex in reader.get_uid():
        hex_raw = hex(non_hex)[2:].upper()
        if len(hex_raw) < 2:
          hex_raw = '0' + hex_raw
        tag_id += hex_raw
    except:
       tag_id = ''

    if  tag_id != '':
      tag_id_good = True
      return tag_id


async def hello(websocket):
  msg = await websocket.recv()

  if msg == "reed_tag_id":
    tag_id = read_card()
    print(f"tag_id <=>", tag_id)
    resp = requests.post(
        'http://localhost:8000/api/card/scan/',
        data={'tag_id': tag_id},
        verify=False
    )
    
    if resp.status_code != 200:
      json_retour = json.dumps({'message': 'NotFound', 'tag_id': ''})
      await websocket.send(json_retour)

    json_retour = json.dumps(resp.json())
    print("Response: ", resp.json())
    await websocket.send(json_retour)

async def main():
  async with serve(hello, "localhost", 8001):
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
  asyncio.run(main())
