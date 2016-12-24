from assertpy import assert_that
from mock import mock

import klimalogger


class TestDataBuilderTest(object):
    def setup(self):
        self.config = mock.Mock()
        self.uut = klimalogger.DataBuilder(self.config)

    def test_data_is_empty_by_default(self):
        assert_that(self.uut.data).is_empty()

    def test_create_entry(self):
        self.config.client_location_name = 'location'
        self.uut.add('<sensor>', '<type>', '<unit>', '<value>', is_calculated=False)

        assert_that(self.uut.data).contains({
            'field' : {'value': '<value>'},
            'tags': {'type': '<type>', 'calculated': False}
        })