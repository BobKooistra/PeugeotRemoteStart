from serial import Serial
from time import sleep


class Starter:
    def open(self):
        self.__connection = Serial("/dev/ttyUSB0", 9600, timeout=1)

    def close(self):
        if self.__connection is not None:
            self.__connection.close()

    def __init__(self):
        self.__connection : Serial = None
        self.open()

    def checkConnection(self):
        i = 0
        while i < 3 and (self.__connection is None or not self.__connection.isOpen()):
            self.open()
            i += 1
        if i == 3:
            raise ConnectionError("Couldn't connect to serial port.")
        self.__connection.flush()

    def on(self):
        self.checkConnection()
        self.__connection.write(b"zaplon_on")

    def off(self):
        self.checkConnection()
        self.__connection.write(b"zaplon_off")

    def foto(self):
        self.checkConnection()
        r = None
        i = 0
        while i < 3:
            try:
                self.__connection.write(b"foto")
                sleep(0.5)
                r = self.__connection.readline()
                if bool(r): break
            except Exception as e:
                if i == 2: raise e
                self.checkConnection()
            finally:
                i += 1
        r = r and int(r.strip())
        return r

    def start(self):
        self.checkConnection()
        f = self.foto()
        if f is not None and f < 10:
            self.__connection.write(b"rozruch")
            sleep(1)
            self.__connection.write(b"700")


