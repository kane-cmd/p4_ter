#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only

import os
import sys

# On importe uniquement ce dont on a besoin pour l'IPv6 basique
from scapy.all import IPv6, TCP, sniff

def handle_pkt(pkt):
    # On filtre : on ne veut QUE les paquets IPv6 + TCP dont le port de destination est 1234
    if IPv6 in pkt and TCP in pkt and pkt[TCP].dport == 1234:
        print("got a packet")
        pkt.show2()
        # hexdump(pkt) # Décommentez cette ligne si vous voulez voir les données brutes en hexadécimal
        sys.stdout.flush()

def main():
    # Recherche dynamique de l'interface réseau (par exemple h2-eth0)
    ifaces = [i for i in os.listdir('/sys/class/net/') if 'eth' in i]
    
    if not ifaces:
        print("Cannot find any eth interface")
        exit(1)
        
    iface = ifaces[0]
    print(f"sniffing on {iface}")
    sys.stdout.flush()
    
    # Lancement du renifleur sur l'interface trouvée
    sniff(iface=iface, prn=lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
