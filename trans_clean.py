import bibtexparser # bibtexparser还有很多其他功能，后续再优化
import csv
import re
from tqdm import tqdm
import numpy as np
import pandas as pd


# 读取bibtex文件，清洗数据，存入metadata.csv
def get_meta_from_bib(bibpath, save_file = 'metadata.csv'):
    with open(bibpath) as bib_file:
        bib_data = bibtexparser.load(bib_file).entries
    bib_file.close()

    with open(save_file, 'w') as file: # 创建csv表，写好表头
        writer = csv.writer(file)
        writer.writerow(['doi', 'title', 'author', 'affiliations', 'abstract', 'keywords', 'journal', 'year', 'month', 'type', 'language', 'categories'])
    file.close()
    
    for i in tqdm(bib_data):
        metadata_list = []
        if 'doi' in i:
            metadata_list.append(i['doi'])
        else:
            metadata_list.append('')
        if 'title' in i:
            output = re.sub(r'\n', ' ', i['title'])
            metadata_list.append(output)
        else:
            metadata_list.append('') 
        if 'author' in i:
            output = re.sub(r' and', '; ', i['author'])
            output = re.sub(r'\n', ' ', output)
            output = re.sub(r' ', '', output)
            output = re.sub(r'and', ';', output)
            metadata_list.append(output)
        else:
            metadata_list.append('') 
        if 'affiliations' in i:
            output = re.sub(r'\n', ' ', i['affiliations'])
            output = re.sub(r'; ', ';', output)
            metadata_list.append(output)
        else:
            metadata_list.append('')
        if 'abstract' in i:
            output = re.sub(r'\n', ' ', i['abstract'])
            # 去掉摘要末尾的license statement
            output = re.sub(r'\(C\)(.*?)reserved.', '', output)
            output = re.sub(r'\(c\)(.*?)reserved.', '', output)
            output = re.sub(r'\(C\)(.*?)Inc.', '', output)
            output = re.sub(r'\(c\)(.*?)Inc.', '', output)
            metadata_list.append(output)
        else:
            metadata_list.append('') 
        if 'keywords' in i:
            output = re.sub(r'\n', ' ', i['keywords'])
            output = re.sub(r'; ', ';', output)
            metadata_list.append(output)
        else:
            metadata_list.append('') 
        if 'journal' in i:
            metadata_list.append(i['journal'])
        else:
            metadata_list.append('')
        if 'year' in i:
            metadata_list.append(i['year'])
        else:
            metadata_list.append('') 
        if 'month' in i:
            metadata_list.append(i['month'])
        else:
            metadata_list.append('') 
        if 'type' in i:
            metadata_list.append(i['type'])
        else:
            metadata_list.append('') 
        if 'language' in i:
            metadata_list.append(i['language'])
        else:
            metadata_list.append('')
        if 'web-of-science-categories' in i:
            output = re.sub(r'\n', ' ', i['web-of-science-categories'])
            output = re.sub(r'; ', ';', output)
            metadata_list.append(output)
        else:
            metadata_list.append('')

        with open(save_file, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(metadata_list)
        file.close()
    
    return None

get_meta_from_bib('savedrecs.bib', save_file = 'metadata.csv')


