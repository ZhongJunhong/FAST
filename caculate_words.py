import json
import pandas as pd

# 读取csv文件，提取某一列的所有行，输出所有其累加得到的string
def join_together(csv_path):
    df0 = pd.read_csv(csv_path, encoding = 'UTF8')
    metadata_list = df0.loc[0:len(df0)]['author'].tolist()

    metadata_str = ''
    for i in metadata_list:
        metadata_str = metadata_str + ';' + str(i)
    # print(metadata_str)
    
    return metadata_str


# 词频统计，输入string，返回dict，key为每个词，value为统计值
def caculate(input_str):
    # input_str = input_str.replace(' ','')
    # input_str = input_str.replace('.','')
    input_str = input_str.split(';')
    count_dict = {}
    for i in input_str:
        if i not in count_dict: # 判断是否不在统计的字典中
            count_dict[i] = 1
        else: # 判断是否不在统计的字典中
            count_dict[i] += 1
    return count_dict

content = sorted(caculate(join_together('metadata.csv')).items(), key = lambda x:x[1])
# print(type(len(content)))
print(content[-(len(content)//15): -1]) # 筛选前15%
