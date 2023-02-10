import json

from unittest import TestCase

from crossref_commons.http_utils import remote_call


class HTTPUtilsTestCase(TestCase):

    def test_remote_call(self):
        code, content = remote_call('https://api.crossref.org', 'works')

        self.assertEqual(code, 200)
        content = json.loads(content)
        self.assertEqual(
            set(content.keys()),
            set(['status', 'message-type', 'message-version', 'message']))
        self.assertEqual(
            set(content['message'].keys()),
            set([
                'total-results', 'items-per-page', 'query', 'facets', 'items'
            ]))
        self.assertTrue(content['message']['total-results'] > 100000000)
        self.assertEqual(content['message']['items-per-page'],
                         len(content['message']['items']))
