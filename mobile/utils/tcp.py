#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from scapy.all import srp, Ether, ARP, conf

def arping(iprange):
    '''
    iprange为ip地址参数，可为单一ip如192.168.1.119或者网段192.168.1.0/24
    本方法的用途为，根据ip地址获取目标机器的MAC地址
    '''
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=iprange), timeout=2)
    collection = []
    for snd, rcv in ans:
        result = rcv.sprintf(r"%ARP.psrc% %Ether.src%").split()
        collection.append(result)
    return collection

#获取指定IP的mac地址的示例
#values = arping('192.168.1.119')
#for ip, mac in values:
#    print ip,mac
