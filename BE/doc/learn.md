# L E A R N 

<h3 style="color:purple;letter-spacing:3px;">2022.5.17</h3>

---

# python-osc

### 创建客户端

```python
import argparse
from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="192.168.43.197",
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
                    help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

client.send_message("/norm", send_data)

connectRequest(2, "vezzzing")
```

### 创建服务端
##### 创建连接对象
```python
import argparse
import json
from pythonosc import dispatcher
from pythonosc import osc_server

parser = argparse.ArgumentParser()
parser.add_argument("--ip",
                    default="192.168.43.197", help="The ip to listen on")
parser.add_argument("--port",
                    type=int, default=5005, help="The port to listen on")
args = parser.parse_args()
dispatcher = dispatcher.Dispatcher()
```
##### 处理函数
```python
# 收到客户端指令的全局处理函数
def global_handler(unused_addr, args):
    current_data = json.loads(args)
    para_allList = norm_handler(current_data)
    # 分析是否有错误
    if para_allList['error']!=0:
        print("不合法的客户端请求")
        server.send_message(json.dumps(para_allList))
    else:
        print("收到请求")
```
##### 开始服务器
```python
# 事件处理列表
dispatcher.map("/norm", global_handler)

server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
print("启动服务端程序: {}".format(server.server_address))
print("开始监听...")
server.serve_forever()
```

