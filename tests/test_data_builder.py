from assertpy import assert_that
from mock import Mock, PropertyMock

import klimalogger


class TestDataBuilderTest(object):
    def setup(self):
        self.config = Mock()
        type(self.config).client_location_name = PropertyMock(return_value='<location>')
        type(self.config).client_host_name = PropertyMock(return_value='<host>')
        self.uut = klimalogger.DataBuilder(self.config)

    def test_data_is_empty_by_default(self):
        assert_that(self.uut.data).is_empty()

    def test_create_entry(self):
        self.uut.add('<sensor>', '<type>', '<unit>', '<value>', is_calculated=False)

        assert_that(self.uut.data).contains({
            'measurement': 'data',
            'tags': {'host': '<host>', 'location': '<location>', 'type': '<type>', 'unit': '<unit>', 'sensor': '<sensor>', 'calculated': False},
            'time': self.uut.timestamp,
            'fields': {'value': '<value>'}
        })