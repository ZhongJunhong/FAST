from unittest import TestCase

from crossref_commons.utils import to_filter_string, parse_filter_string


class UtilsTestCase(TestCase):

    def test_to_filter_string(self):
        self.assertEqual(to_filter_string({}), '')
        self.assertEqual(
            to_filter_string({
                'planet': 'Gallifrey',
                'species': 'Time Lord'
            }), 'planet:Gallifrey,species:Time Lord')

    def test_parse_filter_string(self):
        self.assertEqual(parse_filter_string(None), {})
        self.assertEqual(parse_filter_string(''), {})
        self.assertEqual(
            parse_filter_string('planet:Gallifrey,species:Time Lord'), {
                'planet': 'Gallifrey',
                'species': 'Time Lord'
            })
