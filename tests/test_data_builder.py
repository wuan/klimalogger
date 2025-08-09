from assertpy import assert_that
from mock import Mock, PropertyMock

import klimalogger


class TestDataBuilderTest:

    def setup_method(self):
        self.uut = klimalogger.DataBuilder()

    def test_data_is_empty_by_default(self):
        assert_that(self.uut.data).is_empty()

    def test_create_entry(self):
        self.uut.add('<sensor>', '<type>', '<unit>', '<value>', is_calculated=False)

        assert_that(self.uut.data).contains({
            'measurement': 'data',
            'tags': {'type': '<type>', 'unit': '<unit>', 'sensor': '<sensor>', 'calculated': False},
            'time': self.uut.timestamp,
            'fields': {'value': '<value>'}
        })
