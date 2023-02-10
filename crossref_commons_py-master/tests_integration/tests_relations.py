import re

from unittest import TestCase

from crossref_commons.relations import get_alias, get_directly_related, get_related


class RelationTestCase(TestCase):

    def test_get_alias_empty(self):
        with self.assertRaises(ValueError) as context:
            get_alias(None)
        self.assertTrue('None' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_alias('not-a-doi')
        self.assertTrue('not-a-doi' in context.exception.args[0])

    def test_get_alias(self):
        self.assertIsNone(get_alias('10.5621/sciefictstud.40.2.0382'))
        #self.assertIsNotNone(
        #    re.match('10.\d{4,9}/[\-\._;\(\)\/:A-Z0-9]+',
        #             get_alias('10.12775/pbpis.2019.013')))

    def test_get_directly_related_empty(self):
        with self.assertRaises(ValueError) as context:
            get_directly_related(None)
        self.assertTrue('None' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_directly_related('not-a-doi')
        self.assertTrue('not-a-doi' in context.exception.args[0])

    def test_get_directly_related(self):
        self.assertEqual(
            [], get_directly_related('10.5621/sciefictstud.40.2.0382'))
        self.assertEqual([('10.1101/283119', 'isPreprintOf')],
                         get_directly_related('10.1167/18.8.6'))

    def test_get_related_empty(self):
        with self.assertRaises(ValueError) as context:
            get_related(None)
        self.assertTrue('None' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_related('not-a-doi')
        self.assertTrue('not-a-doi' in context.exception.args[0])

    def test_get_related(self):
        self.assertEqual([], get_related('10.5621/sciefictstud.40.2.0382'))
        self.assertEqual([('10.1101/283119', 'isPreprintOf')],
                         get_related('10.1167/18.8.6'))
