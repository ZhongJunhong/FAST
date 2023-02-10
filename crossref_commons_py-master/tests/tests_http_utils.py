from unittest import TestCase

from crossref_commons.http_utils import uenc


class HTTPUtilsTestCase(TestCase):

    def test_uenc(self):
        self.assertEqual(uenc('10.1002'), '10.1002')
        self.assertEqual(
            uenc('10.1002/(sici)1097-0142(19990301)85:5<1179::aid-cncr23>'
                 '3.0.co;2-i'),
            '10.1002%2F%28sici%291097-0142%2819990301%2985%3A5%3C1179%3A%3A'
            'aid-cncr23%3E3.0.co%3B2-i')
