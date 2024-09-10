from ipaddress import IPv4Address


def is_ipv4_address(addr: str) -> bool:
    try:
        IPv4Address(addr)
        return True
    except ValueError:
        return False
