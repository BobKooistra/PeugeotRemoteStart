import obd


class Monitor:
    def __init__(self):
        self.conn = obd.OBD("/dev/rfcomm0")

    def getSpeed(self):
        return self.conn.query(obd.commands.SPEED).value

    def getRPM(self):
        return self.conn.query(obd.commands.RPM).value

    def close(self):
        self.conn.close()
