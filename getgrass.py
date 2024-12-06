import asyncio
import random
import ssl
import json
import time
import uuid
import requests
import shutil
import sys,base64
import os
try:
   from loguru import logger
   from websockets_proxy import Proxy, proxy_connect
   from fake_useragent import UserAgent
except:
   os.system('py -m pip install requests logger websockets_proxy fake_useragent') 
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent
user_agent = UserAgent(os='windows', platforms='pc', browsers='chrome')
random_user_agent = user_agent.random
async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    #logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            urilist = ["wss://proxy.wynd.network:4444/","wss://proxy.wynd.network:4650/"]
            uri = random.choice(urilist)
            #uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        await websocket.send(send_message)
                        await asyncio.sleep(5)
                await asyncio.sleep(1)
                asyncio.create_task(send_ping())
                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.26.2",
                                "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi"
                            }
                        }
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
              print(str("\033[1;32m Error ",e))

async def main():
    #find user_id on the site in conlose localStorage.getItem('userId') (if you can't get it, write allow pasting)
    _user_id = "2oAZ2uwDNvbJ4CyLdjwgUdi1x3p" #input('Please Enter your user ID: ')
    url = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=protocolipport&format=text&timeout=20000'
    local_proxies = requests.get(url).text.splitlines()
    """    local_proxies = []
    url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt?raw=true'
    for u_i in requests.get(url).text.splitlines():
        local_proxies.append(f'http://{str(u_i)}')"""
    tasks = [asyncio.ensure_future(connect_to_wss(i, _user_id)) for i in local_proxies]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    #letsgo
    asyncio.run(main())
    
