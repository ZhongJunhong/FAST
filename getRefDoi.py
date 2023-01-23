import bibtexparser
import re
import json
import time
from tqdm import tqdm
import numpy as np
from requests import get
from bs4 import BeautifulSoup


# 输入一个存储doi的list，从COCI获得所有citing的doi，去重，并以list形式返回
def getCiting(doi_list):
    error_doi_count = 0 # 无法请求的给定doi
    citing_doi_list = set()
    
    for i in tqdm(doi_list):
        try:    
            API_CALL = 'https://opencitations.net/index/coci/api/v1/citations/' + i
            # HTTP_HEADERS = {"authorization": "YOUR-OPENCITATIONS-ACCESS-TOKEN"}
            content = json.loads(get(API_CALL, timeout = 60).text)
            for c in content:
                citing_doi_list.add(str(c['citing']))
        except:
            error_doi_count = error_doi_count + 1

    citing_doi_list = list(citing_doi_list)
    
    print("%d given articles can not be requested" % error_doi_count)
    print("%d citing articles have be found" % len(citing_doi_list))
    return citing_doi_list


# 输入一个存储doi的list，从COCI获得其所有cited的doi，去重，并以list形式返回
def getCited(doi_list):
    error_doi_count = 0 # 无法请求的给定doi
    cited_doi_list = set()
    
    for i in tqdm(doi_list):
        try:    
            API_CALL = 'https://opencitations.net/index/coci/api/v1/references/' + i
            # HTTP_HEADERS = {"authorization": "YOUR-OPENCITATIONS-ACCESS-TOKEN"}
            content = json.loads(get(API_CALL, timeout = 60).text)
            for c in content:
                cited_doi_list.add(str(c['cited']))
        except:
            error_doi_count = error_doi_count + 1

    cited_doi_list = list(cited_doi_list)
    
    print("%d given articles can not be requested" % error_doi_count)
    print("%d cited articles have be found" % len(cited_doi_list))
    return cited_doi_list


# 对所有找到的doi去重，最后返回一个存储所有doi的list
def together(all_doi_list): # 任意多个存储doi的list，放入一个大list再输入。如 list1 + list2 + list3 + ……
    doi_together = np.array(all_doi_list).tolist()
    print("%d articles before drop duplicated" % len(doi_together))
    
    doi_together = np.unique(doi_together) # 去重
    print("%d articles after drop duplicated" % len(doi_together))

    return doi_together
