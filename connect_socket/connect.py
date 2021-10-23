import websocket


def connect_socket(on_open="", on_close="", on_message="", on_error=""):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/chat/1/", on_message=on_message,
                                on_close=on_close, on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()
    return ws