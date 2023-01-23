from bs4 import BeautifulSoup


# 输入一个doi，从网络爬取，返回abstract和keywords
def get_ab_kw_from_doi(doi, timeout = 30):
    try:
        content = BeautifulSoup(get('https://www.doi.org/' + doi, timeout = timeout).text, 'html.parser')
        url_content = content.find_all('meta')[2]
        red_url = url_content.find('content')
        print(red_url)
        
    except:
        print("Some error occured, please check the input and internet again.")

    return None


# 从crossref调取abstract
def getAb(doi_list): 
    has_abstract_count = 0
    error_doi_count = 0
    no_abstract_key_count = 0

    for i in tqdm(doi_list):
        try:
            API_CALL = 'http://api.crossref.org/works/' + i
            content = json.loads(get(API_CALL, timeout = 30).text)
            # content = json.dumps(content, indent = 4)
            if "abstract" in content:
                content = content['abstract']
                has_abstract_count = has_abstract_count + 1
            else:
                no_abstract_key_count = no_abstract_key_count + 1
        except:
            error_doi_count = error_doi_count + 1
    
    print('%d articles found abstract' % has_abstract_count)
    print('%d articles have no abstract' % no_abstract_key_count)
    print('%d articles can not be requests' % error_doi_count)
    return None



'''
%2F = /
%3A = :
%3F = ?
%25 = %
%3D = =
https://www.sciencedirect.com/science/article/pii/S0165168406001241?via=ihub&amp;key=a03cac0d25e7e1b9e5dac0cf5cf697d999cdb98c
'''