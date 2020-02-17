from serial import Serial
from time import sleep
from obd import Async


class OnGearError(BaseException):
    pass


class Starter:
    def __init__(self, photoresistor_threshold=10):
        self.photoresistor_threshold = photoresistor_threshold
        self.__connection: Serial = None
        self.open_conn()

    def open_conn(self):
        self.__connection = Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.check_connection()

    def close_conn(self):
        if self.__connection is not None:
            self.__connection.close()

    def check_connection(self):
        i = 0
        while i < 3 and (self.__connection is None or not self.__connection.isOpen()):
            self.open_conn()
            i += 1
        if i == 3:
            raise ConnectionError("Couldn't connect to serial port.")
        else:
            self.__connection.flush()

    def on(self):
        self.check_connection()
        self.__connection.write(b"zaplon_on")

    def off(self):
        self.check_connection()
        self.__connection.write(b"zaplon_off")

    def close(self):
        self.check_connection()
        self.__connection.write(b"zamknij")

    def open(self):
        self.check_connection()
        self.__connection.write(b"otworz")

    def is_on_neutral_gear(self):
        self.check_connection()
        r = None
        i = 0
        while i < 3:
            try:
                self.__connection.write(b"foto")
                sleep(0.5)
                r = self.__connection.readline()
                if bool(r):
                    break
            except Exception as e:
                if i == 2:
                    raise e
                self.check_connection()
            finally:
                i += 1
        r = r and int(r.strip())
        return r < self.photoresistor_threshold

    def start(self, starter_time=700):
        self.check_connection()
        f = self.is_on_neutral_gear()
        if f:
            self.__connection.write(bytes(f"rozruch{starter_time}"))
            return True
        else:
            raise OnGearError()
