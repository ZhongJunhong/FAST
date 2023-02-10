import json

from crossref_commons.config import API_URL
from crossref_commons.http_utils import remote_call, uenc
from crossref_commons.types import EntityType, OutputType
from xml.etree import ElementTree


def get_publication_as_json(doi):
    """Retrieve publication in JSON."""
    if doi is None:
        raise ValueError('DOI cannot be None')
    code, result = remote_call(API_URL, 'works/{}'.format(uenc(doi)))
    if code == 404:
        raise ValueError('DOI {} does not exist'.format(doi))
    elif code != 200:
        raise ConnectionError('API returned code {}'.format(code))
    result_message = json.loads(result).get('message')
    return result_message


def get_publication_as_xml(doi):
    """Retrieve publication in XML."""
    if doi is None:
        raise ValueError('DOI cannot be None')
    code, result = remote_call(
        API_URL,
        'works/{}/transform/application/vnd.crossref.unixsd+xml'.format(
            uenc(doi)))
    if code == 404:
        raise ValueError('DOI {} does not exist'.format(doi))
    elif code != 200:
        raise ConnectionError('API returned code {}'.format(code))
    tree = ElementTree.fromstring(result)
    return tree


def get_publication_as_refstring(doi, style):
    """Retrieve formatted reference string for a given DOI."""
    code, ref_string = remote_call(
        API_URL,
        'works/{}/transform'.format(uenc(doi)),
        headers={'Accept': 'text/x-bibliography; style={}'.format(style)})
    if code == 404:
        raise ValueError('DOI {} does not exist'.format(doi))
    elif code != 200:
        raise ConnectionError('API returned code {}'.format(code))
    return ref_string


def get_member_as_json(mid):
    """Retrieve member in JSON."""
    if mid is None:
        raise ValueError('Member cannot be None')
    code, result = remote_call(API_URL, 'members/{}'.format(uenc(mid)))
    if code == 404:
        raise ValueError('Member {} does not exist'.format(mid))
    elif code != 200:
        raise ConnectionError('API returned code {}'.format(code))
    result_message = json.loads(result).get('message')
    return result_message


def get_entity(eid, entity_type, output_type, *argv):
    """Retrieve the entity of given type in given format."""
    if entity_type == EntityType.MEMBER:
        if output_type == OutputType.JSON:
            return get_member_as_json(eid)
        else:
            raise ValueError(
                'Output type {} not supported'.format(output_type))
    elif entity_type == EntityType.PUBLICATION:
        if output_type == OutputType.JSON:
            return get_publication_as_json(eid)
        elif output_type == OutputType.XML:
            return get_publication_as_xml(eid)
        elif output_type == OutputType.REFSTRING:
            return get_publication_as_refstring(eid, *argv)
        else:
            raise ValueError(
                'Output type {} not supported'.format(output_type))
    else:
        raise ValueError('Entity type {} not supported'.format(entity_type))
