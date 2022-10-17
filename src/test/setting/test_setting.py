from src.main.setting.setting import setting_setup, server_setting


def test_setting_setup():
    setting_setup("test")

    assert server_setting.host_name == "localhost"
    assert server_setting.port == 8082
