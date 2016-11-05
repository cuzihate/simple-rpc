# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import commons
from modules import RPC_Client as rpcclient

ip_list = ['172.16.111.130', '172.16.111.131']

def main():
    flag = True
    while flag:
        server_group = []  # 每次返回到这一级菜单清空列表。。放在while上面害苦我了。。
        print('\033[31;1m当前主机组：%s\033[0m' % ip_list)
        usr_inp = commons.input2('请输入主机或者主机组（默认为主机组）:', default=ip_list)
        if usr_inp not in ip_list and usr_inp != ip_list:
            print('\033[31;1m请按照规则输入：单个IP xxx.xxx.xxx or 回车\033[0m')
            continue
        elif usr_inp in ip_list and usr_inp != ip_list:
            server_group.append(usr_inp)
        else:
            server_group = usr_inp
        client = rpcclient.Client(server_group)
        while True:
            a = input('请输入要执行的命令(u返回上一级菜单|q退出)：').strip()
            if a == 'q':
                print('bye~')
                flag = False
                break
            if a == 'u':
                print('返回上一级菜单~')
                break
            print(" [x] Requesting :")
            response = client.call(a)
            for one_of in response:
                print(one_of)


if __name__ == '__main__':
    main()