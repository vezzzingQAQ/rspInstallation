# client&server
import client
import server
# settings
import ipport


class HandShake():
    def __init__(self, sendToIp, sendToPort, localIp, localPort):
        self.client = client.VezClient()
        self.server = server.VezServer()
        self.back_data = None
        self.send_to_ip = sendToIp
        self.send_to_port = sendToPort
        self.local_ip = localIp
        self.local_port = localPort

    def send_message(self, data):
        current_client = client.VezClient()
        current_client.start(self.send_to_ip, self.send_to_port)
        current_client.send_message(data)

        current_server = server.VezServer()
        current_server.start(self.local_ip, self.local_port)
        current_server.activate()
        current_server.handle_request()
        current_server.close()
        self.back_data = current_server.data_back
