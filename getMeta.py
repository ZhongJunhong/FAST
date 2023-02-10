# Get metadata from COCI
import requests

def getMeta(doi):
    # check the doi format
    HTTP_HEADERS = {"authorization": "131e4c20-427b-4027-8627-a1169182b149"}
    try:
        resp = requests.get(
            'https://opencitations.net/index/coci/api/v1/metadata/' + doi,
            verify = False,
            # headers = HTTP_HEADERS,
            timeout = 10
        )
        if resp.status_code == 200:
            print(resp.headers)
            return resp.content
            
        else:
            print(resp.headers)
            print(resp.status_code)
            return None
    
    except Exception as e:
        return e

test_doi = '10.1093/biolinnean/blac047'

print(getMeta(test_doi))