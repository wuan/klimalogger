import socket

from assertpy import assert_that
from mock import Mock

import klimalogger


class TestDataBuilderTest(object):
    def setup(self):
        self.config_parser = Mock()
        self.uut = klimalogger.config.Config(self.config_parser)

    def test_location_name(self):
        self.config_parser.get.return_value = '<location>'

        result = self.uut.client_location_name

        self.config_parser.get.assert_called_once_with('client', 'location_name')
        assert_that(result).is_equal_to('<location>')

    def test_client_host_name(self):
        result = self.uut.client_host_name

        self.config_parser.assert_not_called()
        assert_that(result).is_equal_to(socket.gethostname())

    def test_username(self):
        self.config_parser.get.return_value = '<username>'

        result = self.uut.store_username

        self.config_parser.get.assert_called_once_with('store', 'username')
        assert_that(result).is_equal_to('<username>')

    def test_password(self):
        self.config_parser.get.return_value = '<password>'

        result = self.uut.store_password

        self.config_parser.get.assert_called_once_with('store', 'password')
        assert_that(result).is_equal_to('<password>')

    def test_store_name(self):
        self.config_parser.get.return_value = '<store_name>'

        result = self.uut.store_name

        self.config_parser.get.assert_called_once_with('store', 'name')
        assert_that(result).is_equal_to('<store_name>')

    def test_store_host(self):
        self.config_parser.get.return_value = '<store_host>'

        result = self.uut.store_host

        self.config_parser.get.assert_called_once_with('store', 'host')
        assert_that(result).is_equal_to('<store_host>')

    def test_store_port(self):
        self.config_parser.get.return_value = '5'
        result = self.uut.store_port

        self.config_parser.get.assert_called_once_with('store', 'port')
        assert_that(result).is_equal_to(5)

    def test_log_path(self):
        self.config_parser.get.return_value = '<log_path>'
        result = self.uut.log_path

        self.config_parser.get.assert_called_once_with('log', 'path')
        assert_that(result).is_equal_to('<log_path>')
