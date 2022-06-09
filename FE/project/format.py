# 格式化打印字典和列表
class Formator():
    # 字典格式
    def write_format_object(self, obj: dict, tab_num=0, is_tab=1):
        if is_tab:
            data = ("\t" * tab_num)
        else:
            data = ''
        data += "{\n"
        length = len(obj)
        for key, value in obj.items():
            el_type = type(value)
            length -= 1
            data += ("\t" * (tab_num + 1) + f'"{key}":')
            if el_type == int or el_type == float:
                data += f'{value}'
            elif el_type == list or el_type == set or el_type == tuple:
                data += self.write_format_list(value, tab_num + 1, 0)
            elif el_type == dict:
                data += self.write_format_object(value, tab_num + 1, 0)
            else:
                data += f'"{value}"'
            if length:
                data += ',\n'
            else:
                data += '\n'
        data += ("\t" * tab_num) + "}"
        return data

    # 列表格式化

    def write_format_list(self, array: list or set or tuple, tab_num=0, is_tab=1):
        array = list(array)
        if is_tab:
            data = ("\t" * tab_num)
        else:
            data = ''
        data += "[\n"
        length = len(array)
        for index, value in enumerate(array):
            el_type = type(value)
            data += ("\t" * (tab_num + 1))
            if el_type == int or el_type == float:
                data += f'{value}'
            elif el_type == list or el_type == set or el_type == tuple:
                data += self.write_format_list(value, tab_num + 1, 0)
            elif el_type == dict:
                data += self.write_format_object(value, tab_num + 1, 0)
            else:
                data += f'"{value}"'
            if length != index + 1:
                data += ',\n'
            else:
                data += '\n'
        data += ("\t" * tab_num) + "]"
        return data
