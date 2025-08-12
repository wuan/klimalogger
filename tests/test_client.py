import logging
from types import SimpleNamespace
from unittest import mock

import pytest

import klimalogger


@pytest.fixture()
def dispatcher():
    return mock.Mock()


@pytest.fixture()
def transport():
    return mock.Mock()


@pytest.fixture()
def cfg():
    return mock.Mock()


@pytest.fixture()
def client(dispatcher, transport, cfg):
    return klimalogger.Client(dispatcher, transport, cfg)


def test_measure_returns_timestamp_and_data(client, dispatcher):
    # Fake result from dispatcher.measure()
    result = SimpleNamespace(timestamp=123.4, data=[{"k": "v"}])
    dispatcher.measure.return_value = result

    ts, data = client.measure()

    assert ts == 123.4
    assert data == [{"k": "v"}]
    dispatcher.measure.assert_called_once()


def test_measure_and_store_calls_store_with_measured_data(client, dispatcher, transport):
    # Use a realistic DataBuilder to produce data
    db = klimalogger.DataBuilder()
    db.add("sensorX", "temp", "C", 21.5)
    dispatcher.measure.return_value = db

    client.measure_and_store()

    # transport.store should be called once with the DataBuilder's data
    transport.store.assert_called_once_with(db.data)


def test_store_data_handles_exception_without_raising(client, transport, caplog):
    # Make transport.store raise and verify it is caught and logged
    transport.store.side_effect = RuntimeError("boom")

    caplog.set_level(logging.ERROR, logger="klimalogger")

    # Should not raise
    client.store_data([{"any": "data"}])

    # Error should have been logged
    assert any(
        rec.levelno == logging.ERROR and "error during data transmission" in rec.getMessage()
        for rec in caplog.records
    )
