from unittest import TestCase

from crossref_commons.sampling import generate_sample_args, extend_sample


class SamplingTestCase(TestCase):

    def test_generate_sample_args(self):
        args = generate_sample_args(size=13, queries={'q': 'tr'})
        self.assertEqual([(13, {}, {'q': 'tr'})], args)

        args = generate_sample_args(size=100, filter={'f': 'fr'})
        self.assertEqual([(100, {'f': 'fr'}, {})], args)

        args = generate_sample_args(size=101, queries={'q': 'tr'})
        self.assertEqual([(100, {}, {'q': 'tr'}), (1, {}, {'q': 'tr'})], args)

        args = generate_sample_args(size=233,
                                    queries={'q': 'tr'},
                                    filter={'f': 'fr'})
        self.assertEqual([(100, {
            'f': 'fr'
        }, {
            'q': 'tr'
        }), (100, {
            'f': 'fr'
        }, {
            'q': 'tr'
        }), (33, {
            'f': 'fr'
        }, {
            'q': 'tr'
        })], args)

    def test_extend_sample(self):
        s1 = [{
            'DOI': '123',
            'title': 'Title 123'
        }, {
            'DOI': '124',
            'title': 'Title 124'
        }, {
            'DOI': '123',
            'title': 'Title 123'
        }, {
            'DOI': '125',
            'title': 'Title 125'
        }]
        s2 = [{
            'DOI': '128',
            'title': 'Title 128'
        }, {
            'DOI': '124',
            'title': 'Title 124'
        }, {
            'DOI': '123',
            'title': 'Title 123'
        }, {
            'DOI': '128',
            'title': 'Title 128'
        }]
        sample = extend_sample(s1, s2)
        self.assertEqual(len(sample), 4)
        self.assertTrue({'DOI': '123', 'title': 'Title 123'} in sample)
        self.assertTrue({'DOI': '124', 'title': 'Title 124'} in sample)
        self.assertTrue({'DOI': '125', 'title': 'Title 125'} in sample)
        self.assertTrue({'DOI': '128', 'title': 'Title 128'} in sample)
