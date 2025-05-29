import sys
import threading
import socket
import json
import time
import streamock
import queue

sys.path.append("tests")
sys.path.append("packages/chat")

import countdown

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8010


def test_countdown():
    args = streamock.args()
    mock = streamock.start(args)
    
    lines = countdown.count_to_zero(3)
    countdown.stream(args, lines)

    res = streamock.stop(mock).decode("utf-8")
    
    assert res.startswith('{"output": "3...')
    assert res.find("Go!") != -1


def mock_server(msg_queue, host=SERVER_HOST, port=SERVER_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    msg = json.loads(data.decode("utf-8"))
                    print(msg)
                    msg_queue.put(msg["output"])
                except Exception:
                    pass


def test_main_integration():
    msg_queue = queue.Queue()
    server_thread = threading.Thread(target=mock_server, args=(msg_queue,), daemon=True)
    server_thread.start()

    args = {
        "input": "3",
        "STREAM_HOST": SERVER_HOST,
        "STREAM_PORT": SERVER_PORT
    }
    
    countdown.main(args)

    time.sleep(5)

    received = []
    while not msg_queue.empty():
        received.append(msg_queue.get())

    expected = ["3...\n", "2...\n", "1...\n", "Go!\n"]
    assert received == expected
