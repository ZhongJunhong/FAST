import bibtexparser # bibtexparser还有很多其他功能，后续再优化
import re
import json
import time
from tqdm import tqdm
import numpy as np
from requests import get
from bs4 import BeautifulSoup

# 读取bibtex文件，提取doi，去重，并以list返回
def getDoiFromBib(bibpath):
    doi_list = set()
    no_doi_count = 0 # 计数有多少缺失doi数据
    
    with open(bibpath) as bib_file:
        bib_data = bibtexparser.load(bib_file)
        bib_data = bib_data.entries
    
    for i in bib_data:
        if 'doi' in i:
            doi_list.add(i['doi'])                    
        else:
            no_doi_count = no_doi_count + 1
    
    doi_list = list(doi_list)
    print("%d given articles have no doi" % no_doi_count)
    return doi_list


# 输入一个存储doi的list，从COCI获得所有citing的doi，去重，并以list形式返回
def getCitingDoi(doi_list):
    error_doi_count = 0 # 无法请求的给定doi
    citing_doi_list = set()
    
    for i in tqdm(doi_list):
        try:    
            API_CALL = 'https://opencitations.net/index/coci/api/v1/citations/' + i
            # HTTP_HEADERS = {"authorization": "YOUR-OPENCITATIONS-ACCESS-TOKEN"}
            content = json.loads(get(API_CALL, timeout = 30).text)
            for c in content:
                citing_doi_list.add(str(c['citing']))
        except:
            error_doi_count = error_doi_count + 1

    citing_doi_list = list(citing_doi_list)
    
    print("%d given articles can not be requested" % error_doi_count)
    print("%d citing articles have be found" % len(citing_doi_list))
    return citing_doi_list


# 输入一个存储doi的list，获得其所有cited的doi，去重，并以list形式返回
def getCitedDoi(doi_list):
    error_doi_count = 0 # 无法请求的给定doi
    cited_doi_list = set()
    
    for i in tqdm(doi_list):
        try:    
            API_CALL = 'https://opencitations.net/index/coci/api/v1/references/' + i
            # HTTP_HEADERS = {"authorization": "YOUR-OPENCITATIONS-ACCESS-TOKEN"}
            content = json.loads(get(API_CALL, timeout = 30).text)
            for c in content:
                cited_doi_list.add(str(c['cited']))
        except:
            error_doi_count = error_doi_count + 1

    cited_doi_list = list(cited_doi_list)
    
    print("%d given articles can not be requested" % error_doi_count)
    print("%d cited articles have be found" % len(cited_doi_list))
    return cited_doi_list


# 对所有找到的doi合起来，去重，最后返回一个存储所有doi的list
def together(all_doi_list): # 任意多个存储doi的list，放入一个大list再输入。如 list1 + list2 + list3 + ……
    doi_together = np.array(all_doi_list).tolist()
    print("%d articles before drop duplicated" % len(doi_together))
    
    doi_together = np.unique(doi_together) # doi去重
    print("%d articles after drop duplicated" % len(doi_together))

    return doi_together
    # return all_data


def getAb(doi_list): # 从crossref调取abstract
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
    print('%d articles have no abstract item' % no_abstract_key_count)
    print('%d articles can not be requests' % error_doi_count)
    return None