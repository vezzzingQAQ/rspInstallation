from pythonosc import udp_client
import json

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
        self.client.send_message("/2/push7", json.dumps(data))
