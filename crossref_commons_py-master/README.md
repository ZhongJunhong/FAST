# Crossref Commons

High-level library for getting data from Crossref APIs (REST, XML, ...). Work in progress.

## Installation

    pip3 install crossref-commons

## Usage

### Retrieving entities

Entities of various types can be retrieved by giving their respective IDs:

    import crossref_commons.retrieval
    
    crossref_commons.retrieval.get_publication_as_json('10.5621/sciefictstud.40.2.0382')
    crossref_commons.retrieval.get_publication_as_xml('10.5621/sciefictstud.40.2.0382')
    crossref_commons.retrieval.get_publication_as_refstring('10.5621/sciefictstud.40.2.0382', 'ieee')
    
    crossref_commons.retrieval.get_member_as_json('15')

Equivalently, you can use `get_entity` function to retrieve any type of entity:

    from crossref_commons.retrieval import get_entity
    from crossref_commons.types import EntityType, OutputType
    
    get_entity('10.5621/sciefictstud.40.2.0382', EntityType.PUBLICATION, OutputType.JSON)
    get_entity('10.5621/sciefictstud.40.2.0382', EntityType.PUBLICATION, OutputType.XML)
    get_entity('10.5621/sciefictstud.40.2.0382', EntityType.PUBLICATION, OutputType.REFSTRING, 'ieee')
    
    get_entity('15', EntityType.MEMBER, OutputType.JSON)

### Retrieving relations

Currently, aliases and general relations are supported:

    from crossref_commons.relations import get_related
    
    get_related('10.1167/18.8.6')

### Iterating

It is possible to iterate over publications meeting specific criteria (JSON only):

    from crossref_commons.iteration import iterate_publications_as_json
    
    filter = {'funder': '10.13039/501100000038', 'type': 'journal-article'}
    queries = {'query.author': 'li', 'query.affiliation': 'university'}
    for p in iterate_publications_as_json(max_results=189, filter=filter, queries=queries):
      print(p['DOI'])

### Sampling

Instead of iterating over the items meeting the criteria, in some cases it is better to use a random sample. `get_sample` will automatically handle sizes larger than Crossref REST API's limit of 100:

    from crossref_commons.sampling import get_sample
    
    filter = {'funder': '10.13039/501100000038', 'type': 'journal-article'}
    queries = {'query.author': 'li', 'query.affiliation': 'university'}
    sample = get_sample(size=121, filter=filter, queries=queries)

### Authorization

You can set the Polite information and/or Plus token by creating a file `~/.crapi_key` with the following content:

    {
      "Crossref-Plus-API-Token": "<<Plus API token, for Plus users only>>",
      "User-Agent": "<<polite user agent; including mailto:email address>>",
      "Mailto": "<<email address>>"
    }

Alternatively, the same information can be provided through environment variables `CR_API_PLUS`, `CR_API_AGENT` and `CR_API_MAILTO`.
