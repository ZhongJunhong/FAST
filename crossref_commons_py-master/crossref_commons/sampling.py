import json
import random

from multiprocessing import Pool
from crossref_commons.config import API_URL
from crossref_commons.http_utils import remote_call
from crossref_commons.utils import to_filter_string

SAMPLE_CHUNK_SIZE = 100


def get_sample_chunk(size, filter={}, queries={}):
    if filter:
        queries['filter'] = to_filter_string(filter)
    queries['sample'] = size
    code, results = remote_call(API_URL, 'works', params=queries)
    if code != 200:
        raise ConnectionError('API returned code {}'.format(code))
    results = json.loads(results)
    return results['message']['items']


def generate_sample_args(size=0, filter={}, queries={}):
    sample_count = int(size / SAMPLE_CHUNK_SIZE)
    sizes = [SAMPLE_CHUNK_SIZE] * sample_count
    if size % SAMPLE_CHUNK_SIZE != 0:
        sizes.append(size % SAMPLE_CHUNK_SIZE)
    return [(s, filter, queries) for s in sizes]


def extend_sample(sample, new_sample):
    sample_dict = {}
    [sample_dict.update({s['DOI']: s}) for s in sample]
    [sample_dict.update({s['DOI']: s}) for s in new_sample]
    return list(sample_dict.values())


def get_sample_of_max_size(size=100, filter={}, queries={}):
    args = locals()
    results = []
    with Pool() as pool:
        results = pool.starmap(get_sample_chunk, generate_sample_args(**args))
    results = [item for sublist in results for item in sublist]
    return extend_sample([], results)


def get_sample(size=100, filter={}, queries={}):
    """Extract a sample of a given size meeting the specified criteria."""
    sample = get_sample_of_max_size(size=size, filter=filter, queries=queries)
    while len(sample) < size:
        sample = extend_sample(
            sample,
            get_sample_of_max_size(size=int(1 + size / 2),
                                   filter=filter,
                                   queries=queries))
    return random.sample(sample, size)
