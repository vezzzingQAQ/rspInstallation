import server
import settings
import random
import json
import time
from pythonosc import udp_client
import ipport
import gipoActions


class WarpedServer(server.VezServer):
    clientId = ""
    serverId = ipport.cmObj.server_id
    token = ""
    to_ip = ""
    to_port = -1
    client_timestamp = ""
    # 返还会话
    client = None

    def initClient(self, to_ip, to_port):
        # 生成服务器的client
        self.client = udp_client.SimpleUDPClient(
            to_ip, to_port)
        self.to_ip = to_ip
        self.to_port = to_port

    def check_commandValid(self, data):
        command_str = None
        # 判断命令是否合法
        if "command" in data:
            command_str = data["command"]
        if command_str:
            if command_str in settings.SetObj.COMMAND_LIST:
                print(settings.SetObj.divider)
                print("收到指令:{}".format(command_str))
                print("执行:{}".format(
                    settings.SetObj.COMMAND_LIST[command_str]["printName"]))
                return True
            else:
                print("指令不合法")
                return False
        print("指令为空")
        return False

    def do_command(self, data):
        # 执行相应的命令
        # 先判断命令是否合法再执行这个函数
        # try:
        # 判断是否合法
        if not ("timestamp" in data):
            self.send_error("missInfo")
            return
        self.client_timestamp = data["timestamp"]
        command = data["command"]
        print(settings.SetObj.divider)
        # 根据不同的指令进行相应操作
        if command == "conn":
            if not("id" in data and "server" in data):
                self.send_error("missInfo")
                return
            # 检查server是否正确
            if data["server"] != self.serverId:
                self.send_error("serverNameErr")
                return
            self.clientid = data["id"]
            self.token = self.gen_token()
            print("连接成功")
            print("绑定id:{}".format(self.clientId))
            print("绑定token:{}".format(self.token))
            # 新建客户端返回数据
            send_data = {
                "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                "clientid": self.clientId,
                "timestamp": self.client_timestamp,
                "token": self.token,
            }
            self.send_message(send_data)
        elif command == "run":
            if not("token" in data and "mode" in data and "settings" in data):
                self.send_error("missInfo")
                return
            # 检查token是否正确
            if data["token"] != self.token:
                self.send_error("tokenErr")
                return
            # 检查mode是否正确
            if data["mode"] not in settings.SetObj.MODE_LIST:
                self.send_error("modeErr")
                return
            # 检查settings是否正确
            if data["mode"] != "custom":
                # 因为执行GPIO动作可能会阻塞线程，所以先返回再执行
                self.send_message({
                    "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                    "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                    "timestamp": self.client_timestamp
                })
                # 此处直接根据mode执行相应GPIO动作
                vgo = gipoActions.VG()
                if data["mode"] == "1":
                    vgo.setMode1()
                elif data["mode"] == "2":
                    vgo.setMode2()
                elif data["mode"] == "3":
                    vgo.setMode3()
                elif data["mode"] == "4":
                    vgo.setMode4()
            else:
                # 自定义命令
                # 检查settings
                current_settings = data["settings"]
                if len(current_settings) == 0:
                    self.send_error("noSetting")
                    return
                # 遍历settings检查是否合法
                for setting in current_settings:
                    if not("node" in setting and "power" in setting and "order" in setting and "duration" in setting and "delay" in setting):
                        self.send_error("settingInvalid")
                        return
                # 发送成功信息
                self.send_message({
                    "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                    "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                    "timestamp": self.client_timestamp
                })
                # 遍历settings执行动作
                # print(current_settings)
                vgo = gipoActions.VG()
                vgo.customAction(current_settings)
        elif command == "stop":
            if not("token" in data and "mode" in data):
                self.send_error("missInfo")
                return
            # 检查token是否正确
            if data["token"] != self.token:
                self.send_error("tokenErr")
                return
            # 检查mode是否正确
            if data["mode"] not in settings.SetObj.MODE_LIST:
                self.send_error("modeErr")
                return
            # 发送成功信息
            self.send_message({
                "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                "timestamp": self.client_timestamp
            })
            # 执行停止动作
            vgo = gipoActions.VG()
            vgo.stop()
        elif command == "sensor":
            if not("token" in data and ("enable" in data or "disable" in data)):
                self.send_error("missInfo")
                return
            # 检查token是否正确
            if data["token"] != self.token:
                self.send_error("tokenErr")
                return
            # 根据指令发起动作
            if "enable" in data:
                if not(data["enable"] == 1 or data["enable"] == 2 or data["enable"] == 3):
                    self.send_error("sensorIdErr")
                    return
                vgo = gipoActions.VG()
                current_value = vgo.sensorEnable(data["enable"])
                self.send_message({
                    "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                    "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                    "sensor": data["enable"],
                    "value": current_value,  # 一个数组
                    "timestamp": time.time(),  # 服务端时间戳
                })
            else:
                if not(data["disable"] == 1 or data["disable"] == 2 or data["disable"] == 3):
                    self.send_error("sensorIdErr")
                    return
                vgo = gipoActions.VG()
                vgo.sensorDisable(data["disable"])
                self.send_message({
                    "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                    "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                    "sensor": data["disable"],
                    "timestamp": time.time(),  # 服务端时间戳
                })
        elif command == "quit":
            if not("token" in data):
                self.send_error("missInfo")
                return
            # 检查token是否正确
            if data["token"] != self.token:
                self.send_error("tokenErr")
                return
            # 执行退出动作
            self.clientid = None
            self.token = ""
            # 发送成功信息
            self.send_message({
                "error": settings.SetObj.ERROR_LIST["success"]["errCode"],
                "message": settings.SetObj.ERROR_LIST["success"]["printErr"],
                "timestamp": self.client_timestamp
            })
        else:
            self.send_error("commandErr")
            return
        # except:
        #     print("!!!!!!!!")
        #     print("未知错误")
        #     print("!!!!!!!!")
        #     self.send_error("unknownErr")

    def gen_token(self):
        # 生成8位随机字符串
        token = ""
        for i in range(8):
            token += chr(random.randint(65, 90))
        return token

    def send_error(self, errorType):
        # 根据错误列表返回错误信息
        send_data = {
            "error": settings.SetObj.ERROR_LIST[errorType]["errCode"],
            "message": settings.SetObj.ERROR_LIST[errorType]["printErr"]
        }
        self.send_message(send_data)

    def send_message(self, sendData):
        # 通过服务器的client发送信息
        self.client.send_message(
            settings.SetObj.urlHeader, json.dumps(sendData))

    def global_handler(self, unused_addr, args):
        # 接收到指令的全局处理函数
        try:
            current_data = json.loads(args)
        except:
            self.send_error("jsonDecodeErr")
            return

        print(current_data)
        if self.check_commandValid(current_data):
            self.do_command(current_data)
        else:
            self.send_error("commandErr")
