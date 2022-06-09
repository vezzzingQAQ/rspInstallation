import json

from pythonosc import dispatcher
from pythonosc import osc_server
import settings
from threading import Timer


class VezServer():
    def __init__(self):
        self.server = None
        self.listen_timer = None
        self.max_listen_time = 0.5
        self.data_back = None

    def start(self, from_ip, from_port):
        # 启动服务器
        print(from_ip, from_port)
        current_dispatcher = dispatcher.Dispatcher()
        # 事件处理列表
        current_dispatcher.map(settings.SetObj.urlHeader, self.global_handler)
        self.server = osc_server.ThreadingOSCUDPServer(
            (from_ip, from_port), current_dispatcher)
        print("启动服务端程序: {}".format(self.server.server_address))
        print("开始监听...")

    def listen_count(self):
        # 大于最大等待时间关闭服务器
        print("服务器没有收到数据")
        self.close()

    def activate(self):
        self.listen_timer = Timer(self.max_listen_time, self.listen_count)
        self.listen_timer.start()
        self.server.server_activate()

    def handle_request(self):
        self.server.handle_request()

    def close(self):
        self.server.server_close()

    # 收到客户端指令的全局处理函数
    def global_handler(self, unused_addr, args):
        current_data = json.loads(args)
        self.data_back = current_data
        # 关闭定时器
        self.listen_timer.cancel()
