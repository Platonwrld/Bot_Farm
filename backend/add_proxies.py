from database.interfaces import ProxyInterface
from database.interfaces import TgClientInterface
from random import choice
proxy_ips = []
with open("proxies.txt", 'r') as file:
    for line in file.read().split("\n"):
        proxy_data = line.split(":")
        print(proxy_data)
        proxy_ips.append(proxy_data[0] + proxy_data[1])
        ProxyInterface.create_model(
            "socks5",
            proxy_data[0],
            int(proxy_data[1]),
            proxy_model_username="lUhvJnt9JcXT",
            proxy_model_password="hyperder",
            proxy_model_is_active=True
        )


clients = TgClientInterface.get_all_by_()
proxies = ProxyInterface.get_all_by()
active_proxies = []
for proxy in proxies:
    if proxy.ip + str(proxy.port) in proxy_ips:
        active_proxies.append(proxy.id)
for client in clients:
    proxy_id = choice(active_proxies)
    TgClientInterface.update_model_by_id(
        client.id,
        "proxy_id",
        proxy_id
    )


for proxy in proxies:
    if not proxy.id in active_proxies:
        ProxyInterface.delete_model_by_id(proxy.id)
