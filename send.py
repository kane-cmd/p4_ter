#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only

import random
import sys
from scapy.all import IPv6, TCP, Ether, get_if_hwaddr, get_if_list, sendp

def get_if():
    ifs = get_if_list()
    iface = None
    for i in get_if_list():
        if "eth0" in i:
            iface = i
            break
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():
    if len(sys.argv) < 3:
        print('Utilisation: python3 send.py <ipv6_dest> "<message>"')
        print('Exemple:     python3 send.py fc00::2 "Hello IPv6"')
        exit(1)

    addr = sys.argv[1] # On prend directement l'adresse IPv6 passée en argument
    message = sys.argv[2]
    iface = get_if()

    print(f"Envoi sur l'interface {iface} vers {addr}")
    
    # Construction du paquet : Ethernet / IPv6 / TCP / Message
    # L'adresse MAC de destination 'ff:ff:ff:ff:ff:ff' est utilisée pour simplifier dans les tutos P4
    pkt = Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IPv6(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / message
    
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)

if __name__ == '__main__':
    main()
