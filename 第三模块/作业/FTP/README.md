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

Server端和Client端有许多重复代码，但是考虑到可能会运行在不懂的机器，没有把重复代码抽出来

# 程序实现的功能

1. 用户加密认证

2. 允许多用户登录

3. 每个用户都有自己的家目录，且只能访问自己的家目录

4. 对用户进行磁盘分配，每一个用户的可用空间可以自己设置

5. 允许用户在ftp server上随意切换目录

6. 允许用户查看自己家目录下的文件

7. 允许用户上传和下载，保证文件的一致性（md5）

8. 文件上传、下载过程中显示进度条

9. 文件支持断点续传

# 登录用户信息

| 用户名 |  密码  | 剩余储存空间 |
| :----: | :----: | :----------: |
|  alex  | 123321 |    3045M     |
|  tim   | 123321 |    2021M     |

# 流程图
![](https://note.youdao.com/yws/public/resource/4688ad24ead263c41c0ef40c907be3cc/xmlnote/WEBRESOURCE9d80763983e65d09e0e8df025eb05fbb/3159)