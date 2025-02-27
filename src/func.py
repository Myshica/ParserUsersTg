def get_proxy_object(proxy: str) -> dict:
    __proxy = None
    try:
        one_part = proxy.split("://")
        two_part = one_part[1].split("@")
        ip, port = two_part[1].split(":")
        login, password = two_part[1].split(":")
        __proxy = {
            'proxy_type': one_part[0],
            'addr': ip,
            'port': int(port),
            'username': login,
            'password': password,
            "rdns": True
        }
    except:
        pass
    try:
        ip, port, username, password = proxy.split(":")
        __proxy = {
            'proxy_type': 'http',
            'addr': ip,
            'port': int(port),
            'username': username,
            'password': password,
            "rdns": True
        }
    except:
        pass

    return __proxy