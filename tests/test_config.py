import socket

import pytest
from assertpy import assert_that
from mock import Mock, MagicMock

import klimalogger


class TestDataBuilderTest:

    @pytest.fixture
    def config_parser(self):
        return MagicMock(name="ConfigParser", autospec=True)
    
    @pytest.fixture
    def uut(self, config_parser):
        return klimalogger.config.Config(config_parser)

    def test_location_name(self, config_parser, uut):
        config_parser.get.return_value = '<location>'

        result = uut.client_location_name

        config_parser.get.assert_called_once_with('client', 'location_name')
        assert_that(result).is_equal_to('<location>')

    def test_client_host_name(self, config_parser, uut):
        result = uut.client_host_name

        config_parser.assert_not_called()
        assert_that(result).is_equal_to(socket.gethostname())

    def test_username(self, config_parser, uut):
        config_parser.get.return_value = '<username>'

        result = uut.queue_username

        config_parser.get.assert_called_once_with('queue', 'username')
        assert_that(result).is_equal_to('<username>')

    def test_password(self, config_parser, uut):
        config_parser.get.return_value = '<password>'

        result = uut.queue_password

        config_parser.get.assert_called_once_with('queue', 'password')
        assert_that(result).is_equal_to('<password>')

    def test_queue_host(self, config_parser, uut):
        config_parser.get.return_value = '<queue_host>'

        result = uut.queue_host

        config_parser.get.assert_called_once_with('queue', 'host')
        assert_that(result).is_equal_to('<queue_host>')

    def test_queue_port(self, config_parser, uut):
        config_parser.get.return_value = '5'
        result = uut.queue_port

        config_parser.get.assert_called_once_with('queue', 'port')
        assert_that(result).is_equal_to(5)

    def test_log_path(self, config_parser, uut):
        config_parser.get.return_value = '<log_path>'
        result = uut.log_path

        config_parser.get.assert_called_once_with('log', 'path')
        assert_that(result).is_equal_to('<log_path>')
