import pytest

import klimalogger


class TestBuildConfig:
    def test_build_config_reads_env_on_circuitpython(self, monkeypatch):
        # Force circuitpython branch
        monkeypatch.setattr(
            "klimalogger.config.is_circuitpython", lambda: True, raising=True
        )

        monkeypatch.setenv("MQTT_HOST", "mqtt.local")
        monkeypatch.setenv("MQTT_PORT", "1883")
        monkeypatch.setenv("MQTT_PREFIX", "home/sensors")
        monkeypatch.setenv("MQTT_USERNAME", "user")
        monkeypatch.setenv("MQTT_PASSWORD", "pass")
        monkeypatch.setenv("LOCATION_NAME", "Lab")
        monkeypatch.setenv("ELEVATION", "123")
        monkeypatch.setenv("DEVICE_MAP", "1=sgp30,2=bme680")

        cfg = klimalogger.config.build_config()
        assert isinstance(cfg, klimalogger.config.Config)
        assert cfg.mqtt_host == "mqtt.local"
        assert cfg.mqtt_port == 1883
        assert cfg.mqtt_prefix == "home/sensors"
        assert cfg.mqtt_username == "user"
        assert cfg.mqtt_password == "pass"
        assert cfg.location_name == "Lab"
        assert cfg.elevation == 123
        assert cfg.device_map == {"1": "sgp30", "2": "bme680"}

    def test_build_config_raises_off_circuitpython(self, monkeypatch):
        # Force non-circuitpython branch
        monkeypatch.setattr(
            "klimalogger.config.is_circuitpython", lambda: False, raising=True
        )
        with pytest.raises(RuntimeError):
            klimalogger.config.build_config()
