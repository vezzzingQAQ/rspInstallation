import warpedServer
import ipport

Server=warpedServer.WarpedServer()
# 设置发送信息的地址
Server.initClient(ipport.cmObj.send_to_ip, ipport.cmObj.send_to_port)
Server.start(ipport.cmObj.local_ip,ipport.cmObj.local_port)