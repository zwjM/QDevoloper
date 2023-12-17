import pandas as pd
import json
def parse_to_jsonabel(re_dict):
    """
    将data.py获取到的数据转化为可json化的格式。具体为：
        timestamp转化为str，
        Dataframe转化为dict
    """
    re_dict_dic = {}
    for k,v in re_dict.items():
        v['date'] = v['date'].dt.strftime('%Y-%m-%d')
        re_dict_dic[k]=v.to_dict()
    return re_dict_dic
def parse_response(response):
    """
    将客户端获取到的json数据解析为原格式（ date不转化为timestamp格式）。
    """
    if response.status_code!=200:
        return response.json()['detail']
    content = response.json()
    content_dic = json.loads(content)
    data = {}
    for k,v in content_dic.items():
        data[k] = pd.DataFrame(v)
    return data

