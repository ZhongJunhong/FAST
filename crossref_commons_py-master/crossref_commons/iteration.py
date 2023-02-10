import json

from crossref_commons.config import API_URL
from crossref_commons.http_utils import remote_call
from crossref_commons.utils import to_filter_string


def iterate_publications_as_json(filter={}, queries={}, max_results=1000):
    """Iterate over publications meeting specific criteria."""
    rows = min(1000, max_results)
    if filter:
        queries['filter'] = to_filter_string(filter)
    cursor = '*'
    toreturn = max_results
    while True:
        if toreturn <= 0:
            return
        queries['cursor'] = cursor
        queries['rows'] = min(rows, toreturn)
        code, results = remote_call(API_URL, 'works', params=queries)
        if code != 200:
            raise ConnectionError('API returned code {}'.format(code))
        results = json.loads(results)
        cursor = results['message']['next-cursor']
        if not results['message']['items']:
            return
        for item in results['message']['items']:
            yield item
            toreturn -= 1
            if toreturn <= 0:
                return
