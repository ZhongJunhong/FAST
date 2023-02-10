import os

from unittest import TestCase
from unittest.mock import patch


class AuthorizationTestCase(TestCase):

    @patch('crossref_commons.authorization.CRAPI_KEY_FN',
           os.path.join(os.path.dirname(__file__), 'data/test_crapi_key.json'))
    def test_authorization_params(self):
        import crossref_commons.authorization
        crossref_commons.authorization.crapi_key.cache_clear()
        key = crossref_commons.authorization.crapi_key()

        self.assertEqual(len(key), 3)
        self.assertEqual(key['Crossref-Plus-API-Token'], 'Bearer auth-key')
        self.assertEqual(key['User-Agent'], 'tests; mailto:me@org.org')
        self.assertEqual(key['Mailto'], 'me@org.org')

    @patch('crossref_commons.authorization.CRAPI_KEY_FN',
           os.path.join(os.path.dirname(__file__),
                        'data/test_crapi_key_no_bearer.json'))
    def test_authorization_params_no_bearer(self):
        import crossref_commons.authorization
        crossref_commons.authorization.crapi_key.cache_clear()
        key = crossref_commons.authorization.crapi_key()

        self.assertEqual(len(key), 3)
        self.assertEqual(key['Crossref-Plus-API-Token'], 'Bearer auth-key')
        self.assertEqual(key['User-Agent'], 'tests; mailto:me@org.org')
        self.assertEqual(key['Mailto'], 'me@org.org')

    def clean_env(self):
        keys = ['CR_API_PLUS', 'CR_API_AGENT', 'CR_API_MAILTO']
        dump = {k: v for k, v in os.environ.items() if k in keys}
        for k in keys:
            if k in os.environ:
                del os.environ[k]
        return dump

    def restore_env(self, dump):
        for k, v in dump.items():
            os.environ[k] = v

    @patch('crossref_commons.authorization.CRAPI_KEY_FN',
           os.path.join(os.path.dirname(__file__),
                        'data/test_crapi_key_nonexistent.json'))
    def test_file_not_exists(self):
        import crossref_commons.authorization
        dump = self.clean_env()
        try:
            crossref_commons.authorization.crapi_key.cache_clear()
            key = crossref_commons.authorization.crapi_key()
            self.assertEqual(key, {})
        finally:
            self.restore_env(dump)

    @patch('crossref_commons.authorization.CRAPI_KEY_FN',
           os.path.join(os.path.dirname(__file__),
                        'data/test_crapi_key_nonexistent.json'))
    def test_env_vars(self):
        import crossref_commons.authorization
        dump = self.clean_env()
        self.restore_env({
            'CR_API_PLUS': 'Bearer auth-key',
            'CR_API_AGENT': 'tests; mailto:me@org.org',
            'CR_API_MAILTO': 'me@org.org'
        })
        try:
            crossref_commons.authorization.crapi_key.cache_clear()
            key = crossref_commons.authorization.crapi_key()
            self.assertEqual(len(key), 3)
            self.assertEqual(key['Crossref-Plus-API-Token'], 'Bearer auth-key')
            self.assertEqual(key['User-Agent'], 'tests; mailto:me@org.org')
            self.assertEqual(key['Mailto'], 'me@org.org')
        finally:
            self.restore_env(dump)

    @patch('crossref_commons.authorization.CRAPI_KEY_FN',
           os.path.join(os.path.dirname(__file__),
                        'data/test_crapi_key_nonexistent.json'))
    def test_env_vars_no_bearer(self):
        import crossref_commons.authorization
        dump = self.clean_env()
        self.restore_env({
            'CR_API_PLUS': 'auth-key',
            'CR_API_AGENT': 'tests; mailto:me@org.org',
            'CR_API_MAILTO': 'me@org.org'
        })
        try:
            crossref_commons.authorization.crapi_key.cache_clear()
            key = crossref_commons.authorization.crapi_key()
            self.assertEqual(len(key), 3)
            self.assertEqual(key['Crossref-Plus-API-Token'], 'Bearer auth-key')
            self.assertEqual(key['User-Agent'], 'tests; mailto:me@org.org')
            self.assertEqual(key['Mailto'], 'me@org.org')
        finally:
            self.restore_env(dump)
