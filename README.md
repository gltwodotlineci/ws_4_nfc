## Websocket and basick web server for kiosk

### In this repository you will find a python app that will be able to run a nfc card reeder and reed the card tag_id and via the websocket server it will send a message and the tag_id to the kiosk app's client. It will also recive POST request in its basik python server and send the message to a web socke client that is stated at the kiosk's template app.

### To run the app will need to installe the next dependences.

- downloading the app
- installing pip
- installing and starting virtual envirenement
```bash
git clone https://github.com/gltwodotlineci/ws_4_nfc.git


sudo apt-get install python-pip
Or
sudo apt-get install python3-pip

# virtual envirenement
apt-get update
apt-get install python-virtualenv
OR
apt-get install python3-virtualenv
# initializing and starting virtual envirenement
cd name_repo_github
python -m venv env
OR
python3 -m venv env
source ./env/bin/activate
```
Once we createt our work envirenement now we can install our independences
```bash
pip install requests
pip install websockets
pip install py122u
```

And now we can run our app by the nexts commands
```python
python server_ws_nfc.py
python bsc_http_serv.py
python broadcast_server.py
Or
python3 server_ws_nfc.py
python3 bsc_http_serv.py
python3 broadcast_server.py
```
