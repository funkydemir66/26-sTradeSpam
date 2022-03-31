import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from time import sleep
import threading


extension_info = {
    "title": "26'sTradeSpam",
    "description": "ts: on&off&cho ",
    "version": "0.2",
    "author": "funkydemir66"
}

ext = Extension(extension_info, sys.argv, silent=True)
ext.start()

KATMER = "OpenTrading"

KASAR = "CloseTrading"

kod = ""

sec_kod = sc = False

def konusma(msj):
    global sc, sec_kod

    def main():
        while sc:
            for i in range(256):
                if sc:
                    ext.send_to_server('{out:'+str(KATMER)+'}{i:'+str(kod)+'}')
                    sleep(0.1)
                    ext.send_to_server('{out:'+str(KASAR)+'}')
                    sleep(0.1)

    text = msj.packet.read_string()

    if text == ':ts cho':
        msj.is_blocked = True
        sec_kod = True
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Open a trade to the player you want to trade spam with "}{i:0}{i:30}{i:0}{i:0}')

    if text == ':ts on':
        msj.is_blocked = True
        sc = True
        thread = threading.Thread(target=main)
        thread.start()
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Script: on "}{i:0}{i:30}{i:0}{i:0}')

    if text == ':ts off':
        msj.is_blocked = True
        sc = False
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Script: off "}{i:0}{i:30}{i:0}{i:0}')


def yukle_kod(p):
    global kod, sec_kod

    if sec_kod:
        sec_kod = False
        user_id, _, _ = p.packet.read("iii")
        kod = str(user_id)
        ext.send_to_client('{in:Chat}{i:123456789}{s:"idd: saved "}{i:0}{i:30}{i:0}{i:0}')




ext.intercept(Direction.TO_SERVER, konusma, 'Chat')
ext.intercept(Direction.TO_SERVER, yukle_kod, 'OpenTrading')
