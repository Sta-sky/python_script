import IPy

def is_ipv4_address(ip):
    if ip:
        try:
            res = IPy.IP(ip)
            print(res)
            return True
        except Exception as e:
            print(e, 'cdsaca=====')
            return False

ip = '535'
is_ipv4_address(ip)