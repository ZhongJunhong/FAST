from unittest import TestCase

from crossref_commons.iteration import iterate_publications_as_json


class IterationTestCase(TestCase):

    def test_iterate_all_publications(self):
        returned = 0
        for p in iterate_publications_as_json(max_results=-10):
            returned += 1
        self.assertEqual(returned, 0)

        returned = 0
        for p in iterate_publications_as_json(max_results=0):
            returned += 1
        self.assertEqual(returned, 0)

        returned = 0
        dois = set()
        for p in iterate_publications_as_json(max_results=150):
            returned += 1
            dois.add(p['DOI'])
        self.assertEqual(returned, 150)
        self.assertEqual(len(dois), 150)

        returned = 0
        dois = set()
        for p in iterate_publications_as_json(max_results=2113):
            returned += 1
            dois.add(p['DOI'])
        self.assertEqual(returned, 2113)
        self.assertEqual(len(dois), 2113)

    def test_iterate_filter(self):
        returned = 0
        dois = set()
        for p in iterate_publications_as_json(max_results=3013,
                                              filter={
                                                  'funder':
                                                  '10.13039/100000925',
                                                  'type': 'journal-article'
                                              }):
            returned += 1
            dois.add(p['DOI'])
            self.assertTrue('10.13039/100000925' in
                            [f.get('DOI', '') for f in p['funder']])
            self.assertEqual(p['type'], 'journal-article')
        self.assertEqual(returned, 3013)
        self.assertEqual(len(dois), 3013)

    def test_iterate_query(self):
        returned = 0
        dois = set()
        for p in iterate_publications_as_json(max_results=1013,
                                              queries={
                                                  'query.bibliographic':
                                                  'floyd',
                                                  'query.affiliation':
                                                  'university'
                                              }):
            returned += 1
            dois.add(p['DOI'])
        self.assertEqual(returned, 1013)
        self.assertEqual(len(dois), 1013)

    def test_iterate(self):
        returned = 0
        dois = set()
        for p in iterate_publications_as_json(max_results=1013,
                                              filter={
                                                  'funder':
                                                  '10.13039/501100000038',
                                                  'type': 'journal-article'
                                              },
                                              queries={
                                                  'query.author': 'li',
                                                  'query.affiliation':
                                                  'university'
                                              }):
            returned += 1
            dois.add(p['DOI'])
            self.assertTrue('10.13039/501100000038' in
                            [f.get('DOI', '') for f in p['funder']])
            self.assertEqual(p['type'], 'journal-article')
        self.assertEqual(returned, 1013)
        self.assertEqual(len(dois), 1013)
