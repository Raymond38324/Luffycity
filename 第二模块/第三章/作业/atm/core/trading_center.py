# encoding: utf-8
import time
from .user import User
from log.log import atm_log,shopping_log


class TradingCenter:
    """
    交易中心类。
    实现了需要的各种接口
    """
    def __init__(self, user):
        """
        :param user:<core.user.User object> 用户实例
        """
        self.user = user
        #初始化一个个人的log对象
        self.log = atm_log(self.user.account, "log/each_user_log/%s" % self.user.account)

    def cash_out(self, num):
        """
        :param num:<int> 用户取现的金额
        :return: None
        体现函数
        """
        self.user.balances -= num * (1 + 0.05)
        if self.user.balances >= 0:
            # 用户余额充足就扣钱，不足就提示
            self.log.info("用户{}取现了{}元 cash_out".format(self.user.account, num))
            self.user.save()
            time.sleep(0.3)
        else:
            print("余额不足")

    def display_user(self):
        """
        :return:None
        查询消费流水的函数
        """
        mapping = {
            "2":"shopping",
            "3":"repayment",
            "4":"transfer",
            "5":"cash_out"
        }
        with open("log/each_user_log/%s" % self.user.account) as f:
            user_log = [i.split(" ") for i in f]

        print('''
        输入序号查看日志范围
        1. 全部
        2. 购物日志
        3. 还款日志
        4. 转账日志
        5. 提现日志
        ''')

        choice = input("输入选项：").strip()

        if choice == "1":
            res = [i[:-1] for i in user_log]
        elif choice in ("2","3","4","5"):
            res = [i[:-1] for i in user_log if i[-1].strip() == mapping.get(choice)]

        else:
            res = []
            print("输入的选择有误，请重新输入！")

        if res:
            for i in res:
                print(" ".join(i))
        else:
            print("要查询的数据不存在")




    def transfer(self, out_user, amount):
        """
        :param out_user:<core.user.User object> 用户对象
        :param amount:<int> 用户转账的金额
        :return:None
        转账函数
        """
        if self.user.balances > amount:
            # 用户余额充足就转账 不足就提示
            self.user.balances, out_user.balances = self.user.balances - amount, out_user.balances + amount
            self.log.info("用户{}向用户{}转账了{}元 transfer".format(self.user.account, out_user.account, amount))
            self.user.save()
            out_user.save()
            time.sleep(0.3)
        else:
            print("账户余额不足")

    def reimbursement(self, amount):
        """
        :param amount:<int>还款金额
        :return: None
        还款函数
        """
        self.user.balances += amount
        self.log.info("用户{}还款了{}元 repayment".format(self.user.account, amount))
        time.sleep(0.3)
        self.user.save()

    def shopping(self, money, goods_match):
        """
        :param money:<int> 购物的总消费
        :param goods_match:<list> 购买的商品
        :return: None
        """
        # 购物相当于转账给商场
        self.transfer(User("10000"), money)
        # 个人记录日志 方便查询流水
        self.log.info("用户{}购物消费了{}元,购买的东西有:{} shopping".format(self.user.account, money, ','.join(goods_match)))
        # 商场记录日志方便 后期汇总
        shopping_log.info("用户{}购物消费了{}元,购买的东西有:{} shopping".format(self.user.account, money, ','.join(goods_match)))
        time.sleep(0.3)
