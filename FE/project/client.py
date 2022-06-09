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

    def send_message(self, data):
        self.client.send_message(settings.SetObj.urlHeader, json.dumps(data))
