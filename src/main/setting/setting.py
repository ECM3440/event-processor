import json
from types import SimpleNamespace


class Server:
    host_name: str
    port: int


server_setting = Server()


def setting_setup(profile: str) -> None:
    filepath = "src/main/conf/{}-conf.json".format(profile)

    conf_file = open(filepath, "r")
    conf = json.load(conf_file, object_hook=lambda d: SimpleNamespace(**d))

    server_setting.host_name = conf.server.host_name
    server_setting.port = conf.server.port
