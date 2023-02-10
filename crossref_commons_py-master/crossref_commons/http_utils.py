import logging
import requests
import urllib.parse

from crossref_commons.authorization import crapi_key
from ratelimit import limits

COMMON_HEADERS = crapi_key()


@limits(calls=50, period=1)
def remote_call(url, path, params={}, headers={}):
    """Make a generic remote call."""
    headers.update(COMMON_HEADERS)
    logging.debug('Calling {}/{} with params {} and headers {}'.format(
        url, path, params, headers))
    r = requests.get('{}/{}'.format(url, path), params=params, headers=headers)
    r.encoding = 'UTF-8'
    code = r.status_code
    return code, str(r.text)


def uenc(s):
    """URL-encode a string."""
    return urllib.parse.quote(s, safe='')
