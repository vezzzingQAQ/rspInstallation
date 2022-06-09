import json
from pythonosc import dispatcher
from pythonosc import osc_server
import settings

current_id = ''
current_token = ''
current_server = ''


class VezServer():
    def __init__(self):
        self.server = None

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
        print("命令行按ctrl+c退出")
        self.server.serve_forever()

    # 收到客户端指令的全局处理函数
    def global_handler(self, unused_addr, args):
        current_data = json.loads(args)
        # print(current_data)
