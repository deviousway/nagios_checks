#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
import re
#If you have old python like 2.6 and you get Warning
# SNI (Subject Name Indication) extension to TLS is not available on this platform
#pleas uncomment 2 lines
#import urllib3
#urllib3.disable_warnings()

USERNAME = "<USERNAME>"
PASSWORD = "<PASSWORD>"
login = "login"
LOGIN_URL = "https://<HOSTBILL_URL>/admin/index.php?cmd=hbchat"
URL = "https://<HOSTBILL_URL>admin/index.php?cmd=hbchat"

def main():
    session_requests = requests.session()

    # Get login auth token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='security_token']/@value")))[0]
    # Create payload
    payload = {
        "action": login,
        "username": USERNAME,
        "password": PASSWORD,
        "security_token": authenticity_token
    }
    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))



    tree = html.fromstring(result.content)
    staff_online_text = tree.xpath('//td[@width="100"]/text()')[1]
    staff_online_members_value = tree.xpath('//td[@width="100"]/b/text()')[1]
    if int(staff_online_members_value) > 0:
        print('OK - ' + staff_online_text + ' ' + str(staff_online_members_value))
        exit(0)
    else:
        print('NOT OK ' + staff_online_text + ' ' + str(staff_online_members_value))
        exit(1)
if __name__ == '__main__':
    main()
