import bluetooth


class Scanner:
    def __init__(self, mac):
        self.__mac = mac

    def __discover__(self):
        self.nearby_devices = bluetooth.discover_devices(duration=1, flush_cache=True, lookup_class=False)

    def is_present(self):
        for addr, name in self.nearby_devices:
            if addr == self.__mac:
                return True
        return False
