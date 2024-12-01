# -*- coding: utf-8 -*-
import IPy

def get_ip_list(begin_ip, count, netmask):
    ip_list = '' #用来存放生成的IP地址
    begin_ip = IPy.IP(begin_ip)
    ip_list += str(begin_ip) + '\n' #将第一个地址放入ip_列表中
    if begin_ip.version() == 4:
        for i in range(count):
            ip = IPy.IP(begin_ip)
            new_ip = IPy.IP(ip.ip + 2 ** (32 - netmask))
            begin_ip =  str(new_ip)
            ip_list += begin_ip + '\n'
    else:
        for i in range(count):
            ipv6 = IPy.IP(begin_ip)
            new_ipv6 = IPy.IP(ipv6.ip + 2 ** (128 - netmask))
            begin_ip =  str(new_ipv6)
            ip_list += begin_ip + '\n'
    return ip_list

if __name__ == "__main__":
    begin_ip = '2401:b60:e00e:7121::'
    ipv6_list2  = get_ip_list(begin_ip = begin_ip, count=300, netmask=127)
    print('批量分配互联IPv6地址:')
    print('============================')
    txt = ''
    for i in ipv6_list2.split('\n'):
        print(f'    up ip addr add {i}/64 dev eth0')
        txt += f'    up ip addr add {i}/64 dev eth0\n'

    with open('ipv6.txt', 'w') as f:
        f.write(txt)
    print('============================')
