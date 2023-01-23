from bs4 import BeautifulSoup

# 输入一个doi，返回abstract和keywords
def get_ab_kw_from_doi(doi, timeout = 30):
    try:
        content = BeautifulSoup(get('https://www.doi.org/' + doi, timeout = timeout).text, 'html.parser')
        url_content = content.find_all('meta')[2]
        red_url = url_content.find('content')
        print(red_url)
        
    except:
        print("Some error occured, please check the input and internet again.")

    return None    



'''
%2F = /
%3A = :
%3F = ?
%25 = %
%3D = =
https://www.sciencedirect.com/science/article/pii/S0165168406001241?via=ihub&amp;key=a03cac0d25e7e1b9e5dac0cf5cf697d999cdb98c
'''