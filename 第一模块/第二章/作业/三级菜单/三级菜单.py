menu = {
    '北京': {
        '海淀': {
            '五道口': {
                'soho': {},
                '网易': {},
                'google': {}
            },
            '中关村': {
                '爱奇艺': {},
                '汽车之家': {},
                'youku': {},
            },
            '上地': {
                '百度': {},
            },
        },
        '昌平': {
            '沙河': {
                '老男孩': {},
                '北航': {},
            },
            '天通苑': {},
            '回龙观': {},
        },
        '朝阳': {},
        '东城': {},
    },
    '上海': {
        '闵行': {
            "人民广场": {
                '炸鸡店': {}
            }
        },
        '闸北': {
            '火车站': {
                '携程': {}
            }
        },
        '浦东': {},
    },
    '山东': {},
}
current_node = [menu]  # 初始化节点列表
while True:
    print("1.输入节点名称进入节点:\n2.输入b返回上一级节点：\n3.输入q退出：")
    for item in current_node[-1]: print(item)  # 打印当前节点的所有子节点
    choice = input(">>>").strip()
    if choice == 'q':  # 如果输入的是q,退出
        break
    elif choice == "b":  # 如果输入的是b
        # 如果当前节点列表中有不只一个字典，pop最后一个节点，否则打印已达到最上级节点
        current_node.pop() if len(current_node) > 1 else print("\033[47;31m 已达到最上级节点 \033[0m")
    elif choice in current_node[-1]:  # 如果输入的节点名称是当前字典的key
        # 如果当前节点名称对应的字典不是空字典，在节点列表中append这个字典，否则打印已达到最下级节点
        current_node.append(current_node[-1].get(choice)) if current_node[-1].get(choice) else print(
            "\033[47;31m 已达到最下级节点 \033[0m")
    else:  # 如果输入的数据不是q,b和当前字典的key
        print("\033[47;31m 输入的数据有误 \033[0m")
