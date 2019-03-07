# ATM

## 程序的环境依赖

1. python版本

   python3.7

2. 需要的非标准库的库

   无

## 实现的功能
1. 用户额度 15000或自定义
2. 实现购物商城，买东西加入 购物车，调用信用卡功能进行结账
3. 可以提现，手续费5%
4. 支持多账户登录
5. 支持账户间转账（用户A转账给用户B，A账户减钱、B账户加钱）
6. 记录每月日常消费流水
7. 提供还款功能
8. ATM记录操作日志（使用logging模块记录日志）
9. 提供管理功能，包括添加账户、用户额度，冻结账户等


## 程序的启动方式
1. 进入atm目录
2. python manage.py

## 登陆用户信息

| 账号  |    密码    |   余额   |   身份   |
| :---: | :--------: | :------: | :------: |
| 10001 | admin_user |  31759   |  管理员  |
| 10002 |   123123   | 11996.35 | 普通用户 |

## 程序的运行效果

管理员

![](https://note.youdao.com/yws/public/resource/f96e1c06bc677aa0e026f869f0a1d54d/xmlnote/WEBRESOURCE69ef38b6f442da72559e44f9974429c7/3116)

普通用户

![](https://note.youdao.com/yws/public/resource/f96e1c06bc677aa0e026f869f0a1d54d/xmlnote/WEBRESOURCE7ddd68366611ab27a4a49b88088dab8d/3118)

## 流程图

![](https://note.youdao.com/yws/public/resource/f96e1c06bc677aa0e026f869f0a1d54d/xmlnote/WEBRESOURCEa0dfc2601ac82f8754862339e17ad977/3121)