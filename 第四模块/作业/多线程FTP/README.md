
# 运行环境

平台　Linux 

python版本　python 3.7.2

# 程序的启动方式

先启动Server端

```bash
cd FTP/Server
python3 manage.py
```

在启动Client

将要上传的文件放到Client/Upload_dir

启动客户端

```python
cd FTP/Client
python3 client.py
```

# 程序实现的功能

1. 用户加密认证
2. 允许多用户登录
3. 每个用户都有自己的家目录，且只能访问自己的家目录
4. 对用户进行磁盘分配，每一个用户的可用空间可以自己设置
5. 允许用户在ftp server上随意切换目录
6. 允许用户查看自己家目录下的文件
7. 允许用户上传和下载，保证文件的一致性（md5）
8. 文件上传、下载过程中显示进度条
9. 支持多并发的功能
10. 用锁机制实现了数据安全(不会出现同一用户，同时在不同地方登陆)
11. 使用队列queue模块，实现线程池
12. 允许用户配置最大的并发数，比如允许只有10并发用户
13. 支持断点续传

# 登录用户信息

| 用户名 |  密码  | 剩余储存空间 |
| :----: | :----: | :----------: |
|  alex  | 123321 |    2993M     |
|  tim   | 123321 |    2048M     |
| wusir  | 123321 |    1024M     |

# 流程图

![](https://note.youdao.com/yws/public/resource/352ff61a91ddf415ad27005dafe8f039/xmlnote/WEBRESOURCE18106d53a091d77958f98f9bbc9a7481/3169)