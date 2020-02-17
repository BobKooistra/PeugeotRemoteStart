import obd


class Monitor:
    def __init__(self):
        self.conn = obd.OBD("/dev/rfcomm0")

    def get_speed(self):
        return self.conn.query(obd.commands.SPEED).value

    def get_rpm(self):
        return self.conn.query(obd.commands.RPM).value

    def close(self):
        self.conn.close()
