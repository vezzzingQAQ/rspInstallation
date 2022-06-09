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
        'success': {
            'errCode': 0,
            'printErr': '成功'
        },
        'commandErr': {
            'errCode': 1,
            'printErr': '命令【command选项】不合法或者为空'
        },
        'timestampErr': {
            'errCode': 2,
            'printErr': '时间戳【timestamp】不合法或者为空'
        },
        'missInfo': {
            'errCode': 3,
            'printErr': '缺少必要信息'
        },
        'jsonDecodeErr': {
            'errCode': 4,
            'printErr': 'json解析错误'
        },
        # 连接命令中的
        'serverNameErr': {
            'errCode': 5,
            'printErr': '服务器名称【server】不对'
        },
        # token错误
        'tokenErr': {
            'errCode': 6,
            'printErr': 'token错误'
        },
        # run中的
        'modeErr': {
            'errCode': 7,
            'printErr': '模式【mode】不合法'
        },
        'noSetting': {
            'errCode': 8,
            'printErr': '没有设置项'
        },
        'settingInvalid': {
            'errCode': 9,
            'printErr': '设置项不合法'
        },
        # sensor中的
        'sensorIdErr': {
            'errCode': 10,
            'printErr': '传感器ID数据不合法'
        },
        # 全局错误
        'unknownErr': {
            'errCode': 999,
            'printErr': '未知错误'
        }
    }

    MODE_LIST = {
        '1': {
            'printName': '默认模式1'
        },
        '2': {
            'printName': '默认模式2'
        },
        '3': {
            'printName': '默认模式3'
        },
        '4': {
            'printName': '默认模式4'
        },
        'custom': {
            'printName': '自定义模式'
        }
    }

    LIGHT_PIN = [24, 23, 18, 21, 16, 20]
