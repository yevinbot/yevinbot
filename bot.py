import websocket
import asyncio
from main import Bot

ws = websocket.create_connection("ws://127.0.0.1:5050/")
api = Bot(ws)
asyncio.run(api.send(msg_type='group', send_id=372373654, msg="a test"))
