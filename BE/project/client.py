import time
from pythonosc import udp_client
import json

import settings


class VezClient():
    def __init__(self):
        self.client = None
        self.id = "vezClient"
        self.server = "vezServer"

    def start(self, to_ip, to_port):
        self.client = udp_client.SimpleUDPClient(
            to_ip, to_port)
        print("启动客户端程序")

    def connectRequest(self):
        para_command = "conn"
        para_id = self.id
        para_server = self.server
        para_timestamp = time.time()
        print("发送信息")
        send_data = json.dumps({
            "command": para_command,
            "id": para_id,
            "server": para_server,
            "timestamp": para_timestamp
        })
        self.client.send_message(settings.SetObj.urlHeader, send_data)
