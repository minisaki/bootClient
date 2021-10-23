from connect_socket.connect import connect_socket
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import json
from config.action_config import TypeControl, WebsiteType
from config.base_config import SERVER_DOMAIN
from bot_service.sub_process import run_facebook_process, run_youtube_process


ws = None
def on_message(ws, message):
    print(f'data nhan dc: {message}')
    jso = json.loads(message)

    if jso["type_control"] == TypeControl.APP.value:
        # điều khiển app ở đây

        if jso["app"] == WebsiteType.FACEBOOK.value:
            run_facebook_process(jso)
            ws.send("client da nhan data")

        if jso["app"] == WebsiteType.YOUTUBE.value:
            run_youtube_process()

        if jso["app"] == WebsiteType.TIKTOK.value:
            pass

    if jso["type_control"] == TypeControl.HARDWARE.value:

        # điều khiển phần cứng ở đây
        pass


def on_error(ws,error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    pass


# def send_message(ws, message):
#     ws.send(json.dumps(message))


if __name__ == "__main__":
    # connect_socket(on_open, on_close, on_error, on_message)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://{SERVER_DOMAIN}/ws/chat/1/", on_message=on_message,
                                on_close=on_close, on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()


a = """
{
  "type": 1,
  "app": "facebook",
  "action": 1,
  "facebook_id": "R123123123132"
  "data": {
    "cookie": "sonnh",
  }
}
data:
    id_post : id post dùng để like với action like 

"""
