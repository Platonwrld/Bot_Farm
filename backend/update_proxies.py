from database.interfaces import ProxyInterface


with open("proxies.txt", 'r') as file:
    for line in file:
        proxy_data = line.split(":")
        proxy_model = ProxyInterface.get_first_by_ip(proxy_data[0])
        if proxy_model:
            ProxyInterface.update_model_by_id(
                proxy_model.id,
                "username",
                "6SifrK4YyVNT"
            )
            ProxyInterface.update_model_by_id(
                proxy_model.id,
                "password",
                "hyperder"
            )