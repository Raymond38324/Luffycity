# encoding: utf-8
goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
]


class ShoppingCar:
    def __init__(self, balance, trading_center):
        self.buy_item = []
        self.balance = balance
        self.trading_center = trading_center
        self.amount = 0

    def color_print(self, message, choice="info"):
        """
        :param message:<str> 获取输入的信息
        :param choice: <str> 选择的颜色种类
        :return:
        """
        if choice == "info":
            print("\033[47;36m %s \033[0m" % message)
        elif choice == "error":
            print("\033[47;31m %s \033[0m" % message)

    def shopping(self):
        '''
        打印商品列表，等待用户选择。余额够的时候将商品加入购物车，不够的时候提示。
        输入的商品序号格式错误时，重新调用该函数。
        '''
        for index, item in enumerate(goods, 1):  # 打印商品列表。
            print(index, goods[index - 1])
        try:
            choice = int(input("输入商品序号："))  # 等待用户输入
            if self.balance >= goods[choice - 1]["price"]:  # 余额充足，用户余额减去商品价格，将商品加入购物车。
                self.balance -= goods[choice - 1]["price"]
                self.amount += goods[choice - 1]["price"]
                self.buy_item.append(goods[choice - 1]["name"])
                self.color_print("{}已加入购物车!".format(goods[choice - 1]["name"]))
            else:  # 余额不足，提示用户。
                self.color_print("您的余额不足!")
            return
        except (IndexError, ValueError):  # 输入商品格式错误时，再次调用该函数
            self.color_print("您输入的序号格式错误,请重新输入！", choice="error")
            return self.shopping()

    def display_menu(self):

        print(
            '''
            1.购物
            2.查询已购买商品
            3.结账
            '''
        )
        choice = input("请输入选项序号：")
        if choice == '1':  # 输入1时调用购买商品函数。
            self.shopping()
        elif choice == '2':  # 输入2时打印商品列表。
            print(self.buy_item)
        elif choice == '3':  # 输入3时打印用户信息,调用支付接口，退出程序。
            self.trading_center.shopping(self.amount, self.buy_item)
            return
        else:  # 当输入错误时，提示用户输入错误。
            self.color_print("输入的序号有误！请重新输入", choice="error")
        # 用户没有选择退出时，再次调用该函数
        return self.display_menu()
