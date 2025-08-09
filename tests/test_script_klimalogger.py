import sys
from unittest import mock

import pytest

import klimalogger as kl


@pytest.fixture(autouse=True)
def _no_console_handler(mocker):
    # Avoid touching real logging handlers during CLI tests
    mocker.patch.object(kl, "add_log_handler", side_effect=lambda handler: None)
    if hasattr(kl, "logger"):
        mocker.patch.object(kl.logger, "create_console_handler", side_effect=lambda: None)


def import_cli_module():
    # Import the CLI module fresh to ensure clean state between tests
    import importlib
    return importlib.import_module("klimalogger.script.klimalogger")


def run_main_with_args(args):
    mod = import_cli_module()
    old_argv = sys.argv
    try:
        sys.argv = ["prog"] + args
        return mod.main()
    finally:
        sys.argv = old_argv


def test_default_calls_measure_and_store(mocker, capsys):
    client_mock = mock.Mock()

    mocker.patch.object(kl, "client", return_value=client_mock)

    rc = run_main_with_args([])

    assert rc == 0
    client_mock.measure_and_store.assert_called_once_with()


def test_service_calls_measure_and_store_periodically(mocker):
    client_mock = mock.Mock()

    mocker.patch.object(kl, "client", return_value=client_mock)

    rc = run_main_with_args(["--service"])

    assert rc == 0
    client_mock.measure_and_store_periodically.assert_called_once_with()


def test_check_prints_measure_result(mocker, capsys):
    client_mock = mock.Mock()
    client_mock.measure.return_value = (1234567890, {"temp": 21.5})

    mocker.patch.object(kl, "client", return_value=client_mock)

    rc = run_main_with_args(["--check"])
    captured = capsys.readouterr().out.strip()

    assert rc == 0
    assert "1234567890" in captured
    assert "temp" in captured
    client_mock.measure.assert_called_once_with()


def test_version_prints_version(mocker, capsys):
    # Ensure client() is not called in this path
    mocker.patch.object(kl, "client", side_effect=lambda *a, **k: pytest.fail("client() should not be called for --version"))

    mod = import_cli_module()

    # Replace the imported metadata function used by the module
    mocker.patch.object(mod, "metadata", side_effect=lambda dist: {"Version": "9.9.9"})

    old_argv = sys.argv
    try:
        sys.argv = ["prog", "--version"]
        rc = mod.main()
    finally:
        sys.argv = old_argv

    out = capsys.readouterr().out.strip()
    assert rc == 0
    assert out == "Version 9.9.9"


def test_verbose_and_debug_set_log_level(mocker):
    levels = []
    mocker.patch.object(kl, "set_log_level", side_effect=lambda lvl: levels.append(lvl))

    # verbose case
    levels.clear()
    client_mock = mock.Mock()
    mocker.patch.object(kl, "client", return_value=client_mock)
    rc1 = run_main_with_args(["--verbose"])  # default WARN then INFO
    assert rc1 == 0
    assert len(levels) == 2
    # logging.WARN = 30, logging.INFO = 20, but compare by ordering of calls
    assert levels[-1] == 20  # INFO
    client_mock.measure_and_store.assert_called_once_with()

    # debug case
    levels.clear()
    client_mock = mock.Mock()
    mocker.patch.object(kl, "client", return_value=client_mock)
    rc2 = run_main_with_args(["--debug"])  # default WARN then DEBUG
    assert rc2 == 0
    assert len(levels) == 2
    assert levels[-1] == 10  # DEBUG
    client_mock.measure_and_store.assert_called_once_with()


def test_error_returns_10(mocker, capsys):
    mocker.patch.object(kl, "client", side_effect=RuntimeError("boom"))

    rc = run_main_with_args([])
    out = capsys.readouterr().out

    assert rc == 10
    assert "Error" in out
