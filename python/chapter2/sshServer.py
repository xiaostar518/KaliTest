#!/usr/bin/env python
# coding=utf-8

import socket
import paramiko
import threading
import sys

###############################################
# part.1 使用了Paramiko示例文件中包含的SSH密钥

# 使用Paramiko示例文件的密钥
# host_key = paramiko.RSAKey(filename = 'test_rsa.key')
host_key = paramiko.RSAKey(filename='/root/.ssh/id_rsa')


#################################################
# part.2 使用ssh管道
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        if (username == 'root') and (password == 'lovesthepython'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


server = sys.argv[1]
ssh_port = int(sys.argv[2])

#########################################
# part3 开启套接字监听
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
    # 这里value设置为1,表示将SO_REUSEADDR标记为TURE，
    # 操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，
    # 否则操作系统会保留几分钟该端口。
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))  # 绑定ip和端口
    sock.listen(100)  # 最大连接数为100
    print '[+]Listening for connection...'
    client, addr = sock.accept()
except Exception, e:
    print '[-]Listen failed:' + str(e)
    sys.exit(1)
print '[+]Got a connection!'

################################################
# part4 配置认证模式
try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed'
    chan = bhSession.accept(20)  # 设置超时值为20
    #####################################
    # part5 客户端认证成功
    print '[+] Authenticated!'
    print chan.recv(1024)
    chan.send("Welcome to my ssh")

    ###############################
    # part6 发回ClientConnected消息
    while True:
        try:
            # strip 移除字符串头尾指定的字符串(默认是空格)，这里是换行
            command = raw_input("Enter command:").strip("\n")
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bhSession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bhSession.close()
except Exception, e:
    print '[-] Caught exception:' + str(e)
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)
