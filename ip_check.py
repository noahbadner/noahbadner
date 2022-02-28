#!/usr/bin/python3

import os

from urllib import request, parse

DEVICE_NAME = "home-server"
SIMPLEPUSH_KEY = ""
IP_FILE_PATH = "/home/noahbadner/.ip"


def simplepush_send(key, title="", message="", event=""):
    """A wrapper for the Simplepush api to send a notification to my phone"""
    data = parse.urlencode({'key': key,
                            'title': title,
                            'msg': message,
                            'event': event}).encode()
    req = request.Request("https://api.simplepush.io/send", data=data)
    request.urlopen(req)


def check_ip():
    """Checks the current IP address against the stored IP address"""
    try:
        with open(IP_FILE_PATH, 'r') as ip_file:
            stored_ip_address = ip_file.readline()
    except FileNotFoundError:  # If the file does not exist
        print("No previous IP address found")
        stored_ip_address = None

    current_ip_address = os.popen("curl ifconfig.me").read()

    if stored_ip_address != current_ip_address:
        with open(IP_FILE_PATH, 'w') as ip_file:
            ip_file.write(current_ip_address)

        simplepush_send(SIMPLEPUSH_KEY,
                        f"{DEVICE_NAME} IP Address Change", current_ip_address)


def main():
    """Main method"""
    check_ip()


if  __name__ == "__main__":
    main()

