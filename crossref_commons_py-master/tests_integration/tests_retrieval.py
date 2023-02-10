from unittest import TestCase
from unittest.mock import patch

from crossref_commons.retrieval import get_publication_as_json, \
    get_publication_as_xml, get_publication_as_refstring, get_member_as_json, \
    get_entity
from crossref_commons.types import EntityType, OutputType


class RetrievalTestCase(TestCase):

    def test_get_publication_as_json_empty(self):
        with self.assertRaises(ValueError) as context:
            get_publication_as_json(None)
        self.assertTrue('None' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_publication_as_json('not-a-doi')
        self.assertTrue('not-a-doi' in context.exception.args[0])

    def test_get_publication_as_json(self):
        content = get_publication_as_json('10.5621/sciefictstud.40.2.0382')
        for k in ['source', 'prefix', 'DOI', 'URL', 'member', 'deposited']:
            self.assertTrue(k in content)
        self.assertEqual(content['DOI'].lower(),
                         '10.5621/sciefictstud.40.2.0382')

    def test_get_publication_as_xml_empty(self):
        with self.assertRaises(ValueError) as context:
            get_publication_as_xml(None)
        self.assertTrue('None' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_publication_as_xml('not-a-doi')
        self.assertTrue('not-a-doi' in context.exception.args[0])

    def test_get_publication_as_xml(self):
        ns = '{http://www.crossref.org/xschema/1.1}'
        content = get_publication_as_xml('10.5621/sciefictstud.40.2.0382')
        for k in ['doi', 'publication_date', 'contributors']:
            self.assertIsNotNone(content.iter(ns + k).__next__())
        self.assertEqual(
            content.iter(ns + 'doi').__next__().text.lower(),
            '10.5621/sciefictstud.40.2.0382')

    def test_get_publication_as_refstring_empty(self):
        with self.assertRaises(ValueError) as context:
            get_publication_as_refstring('not-a-doi', 'style')
        self.assertTrue('not-a-doi' in context.exception.args[0])

        with self.assertRaises(ConnectionError) as context:
            get_publication_as_refstring('10.5621/sciefictstud.40.2.0382',
                                         'not-a-style')

    def test_get_publication_as_refstring(self):
        ref_string = get_publication_as_refstring(
            '10.5621/sciefictstud.40.2.0382', 'apa')
        self.assertTrue('.' in ref_string)
        self.assertTrue(',' in ref_string)
        self.assertTrue('(' in ref_string)
        self.assertTrue(')' in ref_string)
        self.assertTrue('10.5621/sciefictstud.40.2.0382' in ref_string)

    def test_get_member_as_json_empty(self):
        with self.assertRaises(ValueError) as context:
            get_member_as_json(None)
        self.assertTrue('None' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_member_as_json('333333333')
        self.assertTrue('333333333' in context.exception.args[0])

    def test_get_member_as_json(self):
        content = get_member_as_json('387')
        for k in ['primary-name', 'prefix', 'id', 'names']:
            self.assertTrue(k in content)
        self.assertEqual(str(content['id']), '387')


class GetEntityTestCase(TestCase):

    @patch('crossref_commons.retrieval.get_publication_as_json')
    def test_get_entity_publication_as_json(self, mock_fun):
        get_entity('10.5621/sciefictstud.40.2.0382', EntityType.PUBLICATION,
                   OutputType.JSON)
        mock_fun.assert_called_once_with('10.5621/sciefictstud.40.2.0382')

    @patch('crossref_commons.retrieval.get_publication_as_xml')
    def test_get_entity_publication_as_xml(self, mock_fun):
        get_entity('10.5621/sciefictstud.40.2.0382', EntityType.PUBLICATION,
                   OutputType.XML)
        mock_fun.assert_called_once_with('10.5621/sciefictstud.40.2.0382')

    @patch('crossref_commons.retrieval.get_publication_as_refstring')
    def test_get_entity_publication_as_refstring(self, mock_fun):
        get_entity('10.5621/sciefictstud.40.2.0382', EntityType.PUBLICATION,
                   OutputType.REFSTRING, 'style')
        mock_fun.assert_called_once_with('10.5621/sciefictstud.40.2.0382',
                                         'style')

    @patch('crossref_commons.retrieval.get_member_as_json')
    def test_get_entity_member_as_json(self, mock_fun):
        get_entity('387', EntityType.MEMBER, OutputType.JSON)
        mock_fun.assert_called_once_with('387')

    @patch('crossref_commons.retrieval.get_publication_as_json')
    @patch('crossref_commons.retrieval.get_publication_as_xml')
    @patch('crossref_commons.retrieval.get_publication_as_refstring')
    @patch('crossref_commons.retrieval.get_member_as_json')
    def test_get_entity_bad_type(self, *mocks):
        with self.assertRaises(ValueError) as context:
            get_entity('id', EntityType.MEMBER, 'not-a-mo-type')
        for m in mocks:
            m.assert_not_called()
        self.assertTrue('not-a-mo-type' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_entity('id', EntityType.PUBLICATION, 'not-a-po-type')
        for m in mocks:
            m.assert_not_called()
        self.assertTrue('not-a-po-type' in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            get_entity('id', 'not-an-entity-type', OutputType.JSON)
        for m in mocks:
            m.assert_not_called()
        self.assertTrue('not-an-entity-type' in context.exception.args[0])
