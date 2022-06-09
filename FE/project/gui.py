# pyqt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import json
from threading import Timer
# 自己搓的模块
import handshake
import format
import ipport
import qssLoader


class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.initUI()

    def center(self):#窗口居中函数
        screen=QDesktopWidget().screenGeometry()#得到屏幕坐标
        size=self.geometry()#得到窗口坐标系
        newLeft=int((screen.width()-size.width())/2)
        newTop=int((screen.height()-size.height())/2)
        self.move(newLeft,newTop)

    def init_ipPort_pan(self):
        # 初始化ip,port输入卡
        self.ipPort_dom = QFrame()
        self.ipPort_dom.setFrameStyle(QFrame.StyledPanel)
        self.ipPort_dom.setProperty("class", "borderFrame")
        self.ipPort_lot = QFormLayout()
        self.localIp_input_dom = QLineEdit(ipport.cmObj.local_ip)
        self.localPort_input_dom = QLineEdit(str(ipport.cmObj.local_port))
        self.serverIp_input_dom = QLineEdit(ipport.cmObj.send_to_ip)
        self.serverPort_input_dom = QLineEdit(str(ipport.cmObj.send_to_port))
        self.ipPort_lot.addRow("本机IP:", self.localIp_input_dom)
        self.ipPort_lot.addRow("本机端口:", self.localPort_input_dom)
        self.ipPort_lot.addRow("服务端IP:", self.serverIp_input_dom)
        self.ipPort_lot.addRow("服务端端口:", self.serverPort_input_dom)
        self.ipPort_dom.setLayout(self.ipPort_lot)

    def init_tabCard_pan(self):
        # 初始化命令选项卡
        self.commandTab_dom = QTabWidget()

        self.conn_tab_dom = QWidget()
        self.run_tab_dom = QWidget()
        self.stop_tab_dom = QWidget()
        self.sensor_tab_dom = QWidget()
        self.quit_tab_dom = QWidget()

        def init_conn_tab_ui():
            mainLayout_lot = QFormLayout()
            # 初始化控件
            self.clientId_input_dom = QLineEdit(ipport.cmObj.client_id)
            self.serverId_input_dom = QLineEdit(ipport.cmObj.server_id)
            self.button_connToServer_dom = QPushButton("连接到服务器")
            self.tokenDisplay_dom = QLabel("????????")
            # 装填控件
            mainLayout_lot.addRow("客户端id", self.clientId_input_dom)
            mainLayout_lot.addRow("服务端id", self.serverId_input_dom)
            mainLayout_lot.addWidget(self.button_connToServer_dom)
            mainLayout_lot.addRow("token", self.tokenDisplay_dom)
            self.conn_tab_dom.setLayout(mainLayout_lot)

        def init_run_tab_ui():
            mainLayout_lot = QFormLayout()
            scrollContainer_dom = QWidget()
            scrollLayout_lot = QFormLayout()
            # 初始化控件
            self.token_input_dom = QLineEdit(self.token)
            self.token_input_dom.setReadOnly(True)
            self.mode_input_dom = QLineEdit("1")
            self.command_scroll_dom = QScrollArea()
            self.command_scroll_dom.setProperty("class", "borderFrame")
            self.command_set_doms = []
            # 快速访问列表
            self.power_set_doms = []
            self.order_set_doms = []
            self.duration_set_doms = []
            self.delay_set_doms = []
            for i in range(16):
                command_set_container = QWidget()
                command_set_layout = QFormLayout()
                widget_list_temp = []
                # 初始化控件
                temp_powerSet_dom = QLineEdit("91")
                temp_orderSet_dom = QLineEdit(str(i+1))
                temp_durationSet_dom = QLineEdit("0.3")
                temp_delaySet_dom = QLineEdit("0")
                widget_list_temp.append(temp_powerSet_dom)  # power
                widget_list_temp.append(temp_orderSet_dom)  # order
                widget_list_temp.append(temp_durationSet_dom)  # duration
                widget_list_temp.append(temp_delaySet_dom)  # delay
                # 装填快速访问列表
                self.power_set_doms.append(temp_powerSet_dom)
                self.order_set_doms.append(temp_orderSet_dom)
                self.duration_set_doms.append(temp_durationSet_dom)
                self.delay_set_doms.append(temp_delaySet_dom)
                # 装填控件
                command_set_layout.addRow("power", widget_list_temp[0])
                command_set_layout.addRow("order", widget_list_temp[1])
                command_set_layout.addRow("duration", widget_list_temp[2])
                command_set_layout.addRow("delay", widget_list_temp[3])
                command_set_container.setLayout(command_set_layout)
                # 装填列表
                self.command_set_doms.append(command_set_container)
                # 装填控件到父组件
                scrollLayout_lot.addRow(
                    "NODE"+str(i+1), self.command_set_doms[i])
            scrollContainer_dom.setLayout(scrollLayout_lot)
            self.button_sendCommand_dom = QPushButton("发送控制指令")
            # 装入scroll_dom
            self.command_scroll_dom.setWidgetResizable(True)
            self.command_scroll_dom.setWidget(scrollContainer_dom)
            # 装填控件
            mainLayout_lot.addRow("token", self.token_input_dom)
            mainLayout_lot.addRow("mode", self.mode_input_dom)
            mainLayout_lot.addRow("settings", self.command_scroll_dom)
            mainLayout_lot.addWidget(self.button_sendCommand_dom)
            self.run_tab_dom.setLayout(mainLayout_lot)

        def init_stop_tab_ui():
            mainLayout_lot = QFormLayout()
            # 初始化控件
            self.token_input1_dom = QLineEdit(self.token)
            self.token_input1_dom.setReadOnly(True)
            self.mode_input1_dom = QLineEdit("1")
            self.button_sendStop_dom = QPushButton("停止运行指令")
            # 装填控件
            mainLayout_lot.addRow("token", self.token_input1_dom)
            mainLayout_lot.addRow("mode", self.mode_input1_dom)
            mainLayout_lot.addWidget(self.button_sendStop_dom)
            self.stop_tab_dom.setLayout(mainLayout_lot)

        def init_sensor_tab_ui():
            mainLayout_lot = QFormLayout()
            # 初始化控件
            self.token_input2_dom = QLineEdit(self.token)
            self.token_input2_dom.setReadOnly(True)
            # 单选按钮框
            self.sensorRadioFrame_dom = QFrame()
            self.sensorRadioFrame_dom.setFrameShape(QFrame.StyledPanel)
            self.sensorRadioFrame_dom.setProperty("class", "borderFrame")
            sensorRadioFrame_lot = QHBoxLayout()
            self.sensorIdBtn1_dom = QRadioButton("距离传感器")
            self.sensorIdBtn1_dom.setChecked(True)
            self.sensorIdBtn2_dom = QRadioButton("温度传感器")
            self.sensorIdBtn2_dom.setEnabled(False)
            self.sensorIdBtn3_dom = QRadioButton("光照传感器")
            self.sensorIdBtn3_dom.setEnabled(False)
            # 添加到lot
            sensorRadioFrame_lot.addWidget(self.sensorIdBtn1_dom)
            sensorRadioFrame_lot.addWidget(self.sensorIdBtn2_dom)
            sensorRadioFrame_lot.addWidget(self.sensorIdBtn3_dom)
            # 装填控件
            self.sensorRadioFrame_dom.setLayout(sensorRadioFrame_lot)
            # 单选按钮框
            self.sensorRadioActionFrame_dom = QFrame()
            self.sensorRadioActionFrame_dom.setFrameShape(QFrame.StyledPanel)
            sensorRadioFrame_lot = QHBoxLayout()
            self.sensorOpen_dom = QRadioButton("打开")
            self.sensorOpen_dom.setChecked(True)
            self.sensorClose_dom = QRadioButton("关闭")
            self.sensorRadioActionFrame_dom.setProperty("class", "borderFrame")
            # 添加到lot
            sensorRadioFrame_lot.addWidget(self.sensorOpen_dom)
            sensorRadioFrame_lot.addWidget(self.sensorClose_dom)
            # 装填控件
            self.sensorRadioActionFrame_dom.setLayout(sensorRadioFrame_lot)
            # 切回正常布局
            self.button_sendSensor_dom = QPushButton("发送指令")
            # 装填控件
            mainLayout_lot.addRow("token", self.token_input2_dom)
            mainLayout_lot.addRow("sensor", self.sensorRadioFrame_dom)
            mainLayout_lot.addRow("action", self.sensorRadioActionFrame_dom)
            mainLayout_lot.addWidget(self.button_sendSensor_dom)
            self.sensor_tab_dom.setLayout(mainLayout_lot)

        def init_quit_tab_ui():
            mainLayout_lot = QFormLayout()
            # 初始化控件
            self.token_input3_dom = QLineEdit(self.token)
            self.token_input3_dom.setReadOnly(True)
            self.button_quitFormServer_dom = QPushButton("从服务器退出")
            # 装填控件
            mainLayout_lot.addRow("token", self.token_input3_dom)
            mainLayout_lot.addWidget(self.button_quitFormServer_dom)
            self.quit_tab_dom.setLayout(mainLayout_lot)

        init_conn_tab_ui()
        init_run_tab_ui()
        init_stop_tab_ui()
        init_sensor_tab_ui()
        init_quit_tab_ui()

        # 绑定到选项卡
        self.commandTab_dom.addTab(self.conn_tab_dom, "conn")
        self.commandTab_dom.addTab(self.run_tab_dom, "run")
        self.commandTab_dom.addTab(self.stop_tab_dom, "stop")
        self.commandTab_dom.addTab(self.sensor_tab_dom, "sensor")
        self.commandTab_dom.addTab(self.quit_tab_dom, "quit")

    def init_commandSend_pan(self):
        # 初始化发送和输入命令框
        self.button_sendJson_dom = QPushButton("发送指令")  # 显示文字
        self.oscCommandSend_dom = QTextEdit("在这里输入命令控制服务端")
        self.oscCommandSend_dom.setFixedHeight(170)

    def init_right_pan(self):
        # 初始化右侧控制面板
        self.init_ipPort_pan()
        self.init_tabCard_pan()
        self.init_commandSend_pan()
        self.panelRight_dom = QFrame()
        self.panelRight_dom.setFrameShape(QFrame.StyledPanel)
        self.panelRight_dom.setProperty("class", "borderFrame")
        panelLayout_lot = QVBoxLayout()
        panelLayout_lot.addWidget(self.ipPort_dom)
        panelLayout_lot.addWidget(self.commandTab_dom)
        panelLayout_lot.addWidget(self.oscCommandSend_dom)
        panelLayout_lot.addWidget(self.button_sendJson_dom)
        self.panelRight_dom.setLayout(panelLayout_lot)

    def init_left_pan(self):
        # 初始化左侧面板
        self.panelLeft_dom = QFrame()
        self.panelLeft_dom.setFrameShape(QFrame.StyledPanel)
        self.panelLeft_dom.setProperty("class", "borderFrame")
        self.codeInputGlobal_dom = QTextEdit("全局代码片段")
        self.codeInputTimed_dom = QTextEdit("间隔执行代码")
        # 按钮组
        ctrlBtnContainer_dom = QFrame()
        ctrlBtnContainer_dom.setFrameShape(QFrame.StyledPanel)
        ctrlBtnContainer_dom.setProperty("class", "borderFrame")
        ctrlBtnContainer_lot = QHBoxLayout()
        ctrlBtnContainer_lot.setProperty("class", "noPadding")
        self.button_runCode_dom = QPushButton("运行代码")
        self.button_runCode_dom.setProperty("class", "noMarginLeft")
        self.button_stopCode_dom = QPushButton("停止运行")
        self.button_stopCode_dom.setProperty("class", "noMarginRight")
        ctrlBtnContainer_lot.addWidget(self.button_runCode_dom)
        ctrlBtnContainer_lot.addWidget(self.button_stopCode_dom)
        ctrlBtnContainer_dom.setLayout(ctrlBtnContainer_lot)
        # 切回
        self.oscDisplayText_dom = QTextEdit("<p>会话会在这里显示(●'◡'●)</p>\
        <p>by <span style='color:rgb(0,0,150)'>vezzzing</span></p>\
        ")
        panelLayout_lot = QVBoxLayout()
        panelLayout_lot.addWidget(self.codeInputGlobal_dom)
        panelLayout_lot.addWidget(self.codeInputTimed_dom)
        panelLayout_lot.addWidget(ctrlBtnContainer_dom)
        panelLayout_lot.addWidget(self.oscDisplayText_dom)
        self.panelLeft_dom.setLayout(panelLayout_lot)
        
    def init_appLayout_pan(self):
        # 设置整体布局
        self.init_right_pan()
        self.init_left_pan()
        self.spt_dom = QSplitter(Qt.Horizontal)
        self.spt_dom.addWidget(self.panelLeft_dom)
        self.spt_dom.addWidget(self.panelRight_dom)
        self.spt_dom.setStretchFactor(0, 6)
        self.spt_dom.setStretchFactor(1, 3)
        self.spt_dom.setProperty("class", "noStroke")
        formlayout_lot = QHBoxLayout()
        formlayout_lot.addWidget(self.spt_dom)
        mainFrame=QWidget()#放置
        mainFrame.setLayout(formlayout_lot)
        self.setCentralWidget(mainFrame)#居中

    def bind_events(self):
        # 绑定响应事件
        self.button_sendJson_dom.clicked.connect(self.act_sendCommand)
        self.button_connToServer_dom.clicked.connect(self.com_conn)
        self.button_sendCommand_dom.clicked.connect(self.com_run)
        self.button_sendStop_dom.clicked.connect(self.com_stop)
        self.button_sendSensor_dom.clicked.connect(self.com_sensor)
        self.button_quitFormServer_dom.clicked.connect(self.com_quit)
        self.button_runCode_dom.clicked.connect(self.start_runCode)
        self.button_stopCode_dom.clicked.connect(self.stop_runCode)

    def init_paras(self):
        # 初始化其他参数
        self.oscDisplayText = ""
        self.clientId = ipport.cmObj.client_id
        self.serverId = ipport.cmObj.server_id
        self.token = ""

    def init_timers(self):
        # 初始化定时器
        self.runCode_timer = QTimer()
        self.runCode_timer.timeout.connect(self.runCode)

    def load_qss(self):
        styleFile = "./project/qss/QssDark1.qss"
        qssStyle = qssLoader.CommonQssLoader.readCss(styleFile)
        self.setStyleSheet(qssStyle)  # 提示文本变红，背景图

    def initUI(self):
        # 总UI入口
        self.setWindowTitle("客 户 端")
        self.setWindowIcon(QIcon("./project/src/ico.jpg"))
        self.resize(1200, 840)
        self.init_paras()
        self.init_timers()
        self.init_appLayout_pan()
        self.bind_events()
        self.load_qss()

    def start_runCode(self):
        # 开始运行代码
        try:
            exec(self.codeInputGlobal_dom.toPlainText())
            self.runCode_timer.start(1000)
        except:
            print("全局错误")

    def stop_runCode(self):
        # 停止运行代码
        self.runCode_timer.stop()

    def runCode(self):
        try:
            def send_msg(msg):
                self.oscCommandSend_dom.setText(json.dumps(msg))
                return_value = self.act_sendCommand()
            exec(self.codeInputTimed_dom.toPlainText())
        except:
            print("代码有错误")

    def act_sendCommand(self):
        hsk = handshake.HandShake(
            self.serverIp_input_dom.text(),
            int(self.serverPort_input_dom.text()),
            self.localIp_input_dom.text(),
            int(self.localPort_input_dom.text())
        )
        try:
            send_data = self.oscCommandSend_dom.toPlainText()
            send_data = json.loads(send_data)
        except:
            self.oscDisplayText += "<p style='color:red'>输入的命令不合法</p>\
                <p style='color:rgb(251,100,0)'><span style='color:rgb(0,100,0)'>参考提示：</span>\
                json格式是不是写错了?</p>"
            self.refresh_comd()
            return
        try:
            hsk.send_message(send_data)
            # 接收信息
            current_formator = format.Formator()
            self.oscDisplayText += "<pre style='color:blue'>{}→".format(self.localIp_input_dom.text()+":"+self.localPort_input_dom.text()) + \
                current_formator.write_format_object(send_data)+"</pre>"
            self.oscDisplayText += "<pre style='color:rgb(0,100,0)'>{}←".format(self.serverIp_input_dom.text()+":"+self.serverPort_input_dom.text()) + \
                current_formator.write_format_object(hsk.back_data)+"</pre>"
            # 设置控件的字符
            self.refresh_comd()
            return hsk.back_data
        except:
            self.oscDisplayText += "<p style='color:red'>服务端未返回数据，或数据解析错误</p>\
                <p style='color:rgb(251,100,0)'><span style='color:rgb(0,100,0)'>参考提示：</span>\
                ip和port写对了吗?网断了吗?服务端跑起来了吗?</p>"
            self.refresh_comd()
            return

    def refresh_comd(self):
        self.oscDisplayText_dom.setText(self.oscDisplayText)
        self.oscDisplayText_dom.moveCursor(QTextCursor.End)

    def com_conn(self):
        # 请求连接到服务器
        self.oscCommandSend_dom.setText(
            json.dumps({
                "command": "conn",
                "id": self.clientId_input_dom.text(),
                "server": self.serverId_input_dom.text(),
                "timestamp": time.time()
            })
        )
        # 更新本地数据
        self.clientId = self.clientId_input_dom.text()
        self.serverId = self.serverId_input_dom.text()
        back_data = self.act_sendCommand()
        if back_data:
            if back_data["error"] == 0:
                self.token = back_data["token"]
                self.oscDisplayText += "<p style='color:black'>连接成功!!</p>"
                self.oscDisplayText += "<p style='color:black'>token=" + self.token+"</p>"
                self.tokenDisplay_dom.setText(self.token)
                self.token_input_dom.setText(self.token)
                self.token_input1_dom.setText(self.token)
                self.token_input2_dom.setText(self.token)
                self.token_input3_dom.setText(self.token)
        self.refresh_comd()

    def com_run(self):
        # 生成settings列表
        current_settings = []
        if self.mode_input_dom.text() == "custom":
            for i in range(16):
                current_settings.append({
                    "node": i+1,
                    "power": self.power_set_doms[i].text(),
                    "order": self.order_set_doms[i].text(),
                    "duration": self.duration_set_doms[i].text(),
                    "delay": self.delay_set_doms[i].text()
                })
        # 请求运行指定硬件
        self.oscCommandSend_dom.setText(
            json.dumps({
                "token": self.token,
                "command": "run",
                "mode": self.mode_input_dom.text(),
                "settings": current_settings,
                "timestamp": time.time()
            })
        )
        # 更新本地数据
        back_data = self.act_sendCommand()
        if back_data:
            if back_data["error"] == 0:
                self.oscDisplayText += "<p style='color:black'>远控成功!!</p>"
        self.refresh_comd()

    def com_stop(self):
        # 停止动作
        self.oscCommandSend_dom.setText(
            json.dumps({
                "token": self.token,
                "command": "stop",
                "mode": self.mode_input1_dom.text(),
                "timestamp": time.time()
            })
        )
        back_data = self.act_sendCommand()
        if back_data:
            if back_data["error"] == 0:
                self.oscDisplayText += "<p style='color:black'>已停止!!</p>"
        self.refresh_comd()

    def com_sensor(self):
        # 传感器动作
        enable_id = 0
        disable_id = 0
        if self.sensorOpen_dom.isChecked():
            if self.sensorIdBtn1_dom.isChecked():
                enable_id = 1
            elif self.sensorIdBtn2_dom.isChecked():
                enable_id = 2
            else:
                enable_id = 3
        else:
            if self.sensorIdBtn1_dom.isChecked():
                disable_id = 1
            elif self.sensorIdBtn2_dom.isChecked():
                disable_id = 2
            else:
                disable_id = 3
        if enable_id != 0:
            self.oscCommandSend_dom.setText(
                json.dumps({
                    "token": self.token,
                    "command": "sensor",
                    "enable": enable_id,
                    "timestamp": time.time()
                })
            )
            back_data = self.act_sendCommand()
            if back_data:
                if back_data["error"] == 0:
                    self.oscDisplayText += "<p style='color:black'>启动成功!!</p>"
                    self.oscDisplayText += "<p style='color:black'>收到的数值:" + \
                        str(back_data["value"])+"</p>"
        else:
            self.oscCommandSend_dom.setText(
                json.dumps({
                    "token": self.token,
                    "command": "sensor",
                    "disable": disable_id,
                    "timestamp": time.time()
                })
            )
            back_data = self.act_sendCommand()
            if back_data:
                if back_data["error"] == 0:
                    self.oscDisplayText += "<p style='color:black'>停止成功!!</p>"
        self.refresh_comd()

    def com_quit(self):
        # 退出
        self.oscCommandSend_dom.setText(
            json.dumps({
                "token": self.token,
                "command": "quit",
                "timestamp": time.time()
            })
        )
        back_data = self.act_sendCommand()
        if back_data:
            if back_data["error"] == 0:
                self.oscDisplayText += "<p style='color:black'>已退出!!</p>"
                self.token = "????????"
                self.tokenDisplay_dom.setText(self.token)
                self.token_input_dom.setText(self.token)
                self.token_input1_dom.setText(self.token)
                self.token_input2_dom.setText(self.token)
                self.token_input3_dom.setText(self.token)
        self.refresh_comd()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainForm()
    main.show()

    sys.exit(app.exec_())
