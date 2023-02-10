from crossref_commons.retrieval import get_publication_as_xml


def get_alias(doi):
    """Get the prime DOI of the given DOI."""
    xml = get_publication_as_xml(doi)
    alias = xml.findall(
        './/c:crm-item[@name="prime-doi"]',
        namespaces={'c': 'http://www.crossref.org/qrschema/3.0'})
    return None if not alias else alias[0].text


def get_directly_related(doi):
    xml = get_publication_as_xml(doi)
    related = xml.findall(
        './/c:crm-item[@name="relation"]',
        namespaces={'c': 'http://www.crossref.org/qrschema/3.0'})
    return [(r.text, r.attrib['claim']) for r in related]


def get_related(doi):
    """Get the DOIs related to the given DOI."""
    relations = []
    alias = get_alias(doi)
    if alias is not None:
        relations.append((alias, 'alias'))
    relations.extend(get_directly_related(doi))
    return relations
