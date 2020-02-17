from flask import Flask, request

from monitor import Monitor
from starter import Starter, OnGearError


class RemoteStartAPI:
    app = Flask(__name__)

    def __init__(self):
        self.__starter = Starter()
        self.__monitor = Monitor()

        self.__register_url_rules()

    def __register_url_rules(self):
        self.app.add_url_rule("/", "hello", self.root)
        self.app.add_url_rule("/ignition_on", "ignition_on", self.ignition_on)
        self.app.add_url_rule("/ignition_off", "ignition_off", self.ignition_off)
        self.app.add_url_rule("/doors_open", "doors_open", self.doors_open)
        self.app.add_url_rule("/doors_close", "doors_close", self.doors_close)
        self.app.add_url_rule("/neutral_gear", "neutral_gear", self.neutral_gear)
        self.app.add_url_rule("/engine_start", "engine_start", self.engine_start)
        self.app.add_url_rule("/speed", "speed", self.speed)
        self.app.add_url_rule("/rpm", "rpm", self.rpm)

    @staticmethod
    def root():
        return "Rzabol says hello."

    @staticmethod
    def run_with_connection_error_check(f, *args, **kwargs):
        try:
            f(*args, **kwargs)
            return
        except ConnectionError as e:
            return {"Error": str(e)}, 500

    def ignition_on(self):
        return self.run_with_connection_error_check(self.__starter.ignition_on)

    def ignition_off(self):
        return self.run_with_connection_error_check(self.__starter.ignition_off)

    def doors_open(self):
        return self.run_with_connection_error_check(self.__starter.doors_open)

    def doors_close(self):
        return self.run_with_connection_error_check(self.__starter.doors_close)

    def neutral_gear(self):
        try:
            neutral = self.__starter.is_on_neutral_gear()
            return {"Neutral": bool(neutral)}
        except ConnectionError as e:
            return {"Error": str(e)}, 500

    def engine_start(self):
        time = request.args.get("time", None)
        try:
            if time is not None:
                self.__starter.engine_start(time)
            else:
                self.__starter.engine_start()
        except ConnectionError as e:
            return {"Error": str(e)}, 500
        except OnGearError:
            return {"Error": "Car is on gear!"}, 409
        else:
            return

    def speed(self):
        return {"speed": self.__monitor.getSpeed()}

    def rpm(self):
        return {"rpm": self.__monitor.getRPM()}

    def run(self):
        self.app.run()

    def __del__(self):
        self.__monitor.close()
        self.__starter.close_conn()


if __name__ == '__main__':
    s = RemoteStartAPI()
    s.run()
