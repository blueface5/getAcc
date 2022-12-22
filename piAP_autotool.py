import os,time,sys,subprocess

print("[!] piAP autotool")
time.sleep(1)
if os.getuid() != 0:
    print("You need root permissions to run this script. Try again with sudo.")
if os.getuid() == 0:
    while 1:
        z=input("> ")
        if z == "help":
            print("""
        check                                          checks for required apps
        set [SSID/PASSWORD/INTERFACE/COUNTRY_CODE]     sets ssid or password or interface of the AP
        print                                          print the variable of ssid or password
        run                                            run the script
        exit                                           quit the script
        """)
        if z in ["set ssid","set SSID"]:
            global ssid
            ssid=z.split("ssid",1)[1]
            ssid=ssid.replace(" ","")
            print("SSID => " + ssid)
        if z in "set PASSWORD":
            global password
            password=z.split("PASSWORD",1)[1]
            password=password.replace(" ","")
            print("PASSWORD => " + password)
        if z in "set INTERFACE":
            global interface
            interface=z.split("set INTERFACE",1)[1]
            interface=interface.replace(" ","")
        if z in "set COUNTRY_CODE":
            global country_code
            country_code=z.split("set COUNTRY_CODE",1)[1]
            country_code=country_code.replace(" ","")
        if z in "print SSID":
            if locals() in 'ssid':
                print("SSID => " + ssid)
            else:
                print("SSID not set.")
        if z in "print PASSWORD":
            if 'password' in locals():
                print("PASSWORD => " + password)
            else:
                print("PASSWORD not set.")
        if z in "print INTERFACE":
            if 'interface' in locals():
                print("INTERFACE => " + interface)
            else:
                print("INTERFACE not set.")
        if z in "print COUNTRY_CODE":
            if 'country_code' in locals():
                print("COUNTRY_CODE => " + country_code)
            else:
                print("COUNTRY_CODE not set.")
        if "exit" in z:
            exit()
        #####################
        if "check" in z:
            check_dnsmasq = subprocess.Popen("apt-cache policy dnsmasq | grep 'Installed: '", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            check_hostapd = subprocess.Popen("apt-cache policy hostapd | grep 'Installed: '", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            check_netfilter = subprocess.Popen("apt-cache policy netfilter-persistent | grep 'Installed: '", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            check_iptables = subprocess.Popen("apt-cache policy iptables-persistent | grep 'Installed: '", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            if b"none" not in check_dnsmasq:
                print("[!] dnsmasq is already installed.")
            if b"none" not in check_hostapd:
                print("[!] hostapd is already installed.")
            if b"none" not in check_netfilter:
                print("[!] netfilter-persistent is already installed.")
            if b"none" not in check_iptables:
                print("[!] iptables-persistent is already installed")
            if b"(" in check_dnsmasq:
                print("[!] dnsmasq is not installed, installing it now.")
                subprocess.Popen("sudo apt install dnsmasq", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                print("[!] dnsmasq is installed.")
            if b"(" in check_hostapd:
                print("[!] hostapd is not installed, installing it now.")
                subprocess.Popen("sudo apt install dnsmasq", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                print("[!] hostapd is installed.")
            if b"(" in check_netfilter:
                print("[!] netfilter-persistent is not installed, installing it now.")
                subprocess.Popen("sudo apt install netfilter-persistent", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                print("[!] netfilter-persistent is installed.")
            if b"(" in check_iptables:
                print("[!] iptables-persistent is not installed, installing it now.")
                subprocess.Popen("sudo apt install iptables-persistent", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                print("[!] iptables-persistent is installed.")
            if locals() in 'ssid':
                print("SSID => " + ssid)
            else:
                print("SSID not set.")
            if 'password' in locals():
                print("PASSWORD => " + password)
            else:
                print("PASSWORD not set.")
            if 'interface' in locals():
                print("INTERFACE => " + interface)
            else:
                print("INTERFACE not set.")
            if 'country_code' in locals():
                print("COUNTRY_CODE => " + country_code)
            else:
                print("COUNTRY_CODE not set.")
        if "run" in z:
            print("[!] Writing dhcpcd config file...")
            subprocess.Popen('echo "interface '+ interface +'\n   static ip_address=192.168.4.1/24\n   nohook wpa_supplicant" >> /etc/dhcpcd.conf', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print("[!] Writing routed-ap config file...")
            subprocess.Popen('echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print("[!] Adding firewall rule...")
            subprocess.Popen('sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print("[!] Saving it...")
            subprocess.Popen('sudo netfilter-persistent save', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print('[!] Changing "dnsmasq.conf" to "dnsmasq.conf.old"...')
            subprocess.Popen('sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print('[!] Writing dnsmasq config...')
            subprocess.Popen('echo -e "interface='+ interface +'\ndhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h\ndomain=wlan\naddress=/gw.wlan/192.168.4.1" > /etc/dnsmasq.conf', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print('[!] Ensuring wireless operation...')
            subprocess.Popen('sudo rfkill unblock wlan', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print('[!] Writing hostapd config...')
            subprocess.Popen('echo -e "country_code='+ country_code +'\ninterface='+ interface +'\nssid='+ ssid + '\nhw_mode=g\nchannel=7\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_passphrase='+ password +'\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP\n" > /etc/dnsmasq.conf', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            print("[!] Done. Rebooting in 3 seconds...")
            time.sleep(3)
