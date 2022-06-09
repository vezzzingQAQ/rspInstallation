class SetObj():
    urlHeader = "/jsonmsg"
    divider = ">>>>>>>>>>>>>>>>>"

    COMMAND_LIST = {
        'conn': {
            'printName': '请求连接到服务端'
        },
        'quit': {
            'printName': '请求中断与服务端连接'
        },
        'run': {
            'printName': '请求节点指令'
        },
        'stop': {
            'printName': '请求停止节点指令'
        },
        'sensor': {
            'printName': '请求获取传感器数据'
        }
    }

    ERROR_LIST = {
        'commandErr': {
            'errCode': 1,
            'printErr': '命令【command选项】不合法或者为空'
        },
        'timestampErr': {
            'errCode': 2,
            'printErr': '时间戳【timestamp】不合法或者为空'
        }
    }
