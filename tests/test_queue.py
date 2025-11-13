import json

import pytest

from klimalogger.config import Config
from klimalogger.transport import QueueTransport


class DummyClient:
    def __init__(self):
        self._connected = True
        self.published = []
        self.on_connect = None
        self.on_disconnect = None
        self.connect_calls = 0
        self.loop_started = False
        self.reconnect_calls = 0
        self.disconnected = False

    def connect(self, host, port):
        # record but do nothing
        self.connect_calls += 1

    def loop_start(self):
        self.loop_started = True

    def is_connected(self):
        return self._connected

    def reconnect(self):
        self.reconnect_calls += 1
        self._connected = True

    def publish(self, topic, payload, qos):
        self.published.append((topic, payload, qos))
        # emulate paho return where result[0] is status code 0 for success
        return (0,)

    def disconnect(self):
        self.disconnected = True
        self._connected = False


@pytest.fixture
def cfg():
    return Config(
        mqtt_host="example.local", mqtt_port=1883, mqtt_prefix="my/prefix", mqtt_qos=2
    )


@pytest.fixture
def patch_client(monkeypatch):
    dummy = DummyClient()
    # Patch the paho client constructor used by our module to return our dummy
    monkeypatch.setattr(
        "klimalogger.transport.mqtt_client.Client", lambda *a, **k: dummy
    )
    return dummy


def build_entry(
    ts=1234567890,
    value=42.5,
    unit="C",
    sensor="foo",
    type_="temperature",
    calculated=False,
):
    return {
        "time": ts,
        "fields": {"value": value},
        "tags": {
            "unit": unit,
            "sensor": sensor,
            "type": type_,
            "calculated": calculated,
        },
    }


def test_map_entry_builds_topic_and_json(cfg, patch_client):
    store = QueueTransport(cfg)
    topic, message = store.map_entry(build_entry(ts=111, value=12.34, unit="%"))
    assert topic == "my/prefix/temperature"
    assert message == {
        "time": 111,
        "value": 12.34,
        "unit": "%",
        "sensor": "foo",
        "calculated": False,
    }


def test_store_publishes_and_reconnects_if_needed(cfg, patch_client):
    dummy = patch_client
    dummy._connected = False  # force reconnect path
    store = QueueTransport(cfg)

    entries = [
        build_entry(ts=1, value=1.0, type_="t"),
        build_entry(ts=2, value=2.0, type_="h"),
    ]

    store.store(entries)

    # reconnect attempted once
    assert dummy.reconnect_calls == 1
    # Two messages published with qos from configuration
    assert len(dummy.published) == 2
    topics = [t for (t, p, q) in dummy.published]
    payloads = [p for (t, p, q) in dummy.published]
    qos_values = [q for (t, p, q) in dummy.published]

    assert topics == ["my/prefix/t", "my/prefix/h"]
    # validate payload JSON round-trip
    decoded = [json.loads(p) for p in payloads]
    assert decoded[0]["value"] == 1.0 and decoded[0]["time"] == 1
    assert decoded[1]["value"] == 2.0 and decoded[1]["time"] == 2
    assert qos_values == [2, 2]


def test_store_raises_when_client_unavailable(cfg, monkeypatch):
    # Make client constructor raise so QueueStore.client becomes None
    def boom(*a, **k):
        raise RuntimeError("no mqtt")

    monkeypatch.setattr("klimalogger.transport.mqtt_client.Client", boom)

    store = QueueTransport(cfg)
    with pytest.raises(RuntimeError):
        store.store([build_entry()])


def test_del_disconnects_when_client_present(cfg, patch_client):
    dummy = patch_client
    store = QueueTransport(cfg)

    # Call the destructor explicitly to verify disconnect is triggered
    store.__del__()
    assert dummy.disconnected is True
