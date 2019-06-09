import socket, struct, fcntl  # fcntl is unix only

def get_nics():
    return socket.if_nameindex()

def get_hw_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15],'utf-8'))
    )[20:24])

def get_ip_addresses():
    ip_addresses = {}
    res = get_nics()
    for r in res:
        ip_addresses[r[1]] = get_hw_addr(r[1])
    return ip_addresses

