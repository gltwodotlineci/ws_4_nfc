import json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
hostname = "127.0.0.1"
port = 8005

# web socket dependences:
import asyncio
import websockets

# the given curl:
# curl -sk -d "bill=20" http://127.0.0.1:8005/bill


async def send_bill(bill_dt):
    uri = "ws://127.0.0.2:8002"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")       
        # await websocket.send(f"The data is: {dt}")
        # send_dt = {'uuid': None, 'amount': None, 'bill': bill_dt}
        json_retour = json.dumps({'message': 'Bill', 'bill': bill_dt})
        await websocket.send(json_retour)


# creating server class
class BillServer(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/bill":
            # Geting and parsing Data            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            decoded_post_data = post_data.decode('utf-8')   
            parsed_post_data = parse_qs(decoded_post_data)
            bill = parsed_post_data.get('bill')[0]
            if bill in ['5','10','20', '50', '100']:
                self.send_response(200)
                print(f"Given bill :  {bill}")
                try:
                    asyncio.run(send_bill(bill))
                except Exception as e:
                    print(f"Connection failed: {e}")

            self.send_response(400)


# starting the server
if __name__ == "__main__":
    webServer = HTTPServer((hostname,port),BillServer)
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print(" Server stopped")
