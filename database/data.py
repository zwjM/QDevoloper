import os

import duckdb
import numpy as np
import pandas as pd

def stock_data(path: str, code_list: list, period: str='1d', start: str='', end: str='', field: list='*', target: str='data') -> dict:
    '''
    获取股票的相关数据\n
    path: 数据位置
    code_list: 需要的股票列表，需要有市场类型后缀 e.g. [000001.SZ]
    period: 1d 5m 1m tick(目前还没有)
    field: list，看图片选择需要的项，或者 使用默认值 获取所有
    start/end: YYYY-MM-DD 格式， 默认获取所有
    target: data or content data获取数据， content忽略所有选项，返回当前数据库包含的股票
    '''

    path = path if path[-1] != '/' else path[:-1]

    path = path + '/STOCK'
    if not os.path.exists(path):
        raise Exception('path 错误')
    
    path = path + f'/{period}'
    if not os.path.exists(path):
        raise Exception('period 错误')

    if target not in ['data', 'content']:
        raise Exception('target 取值错误')
    
    data_dir = path + '/stock.duckdb'
    re_dict = {}
    con = duckdb.connect(database=data_dir)
    if code_list == '*':
        code_list = list(con.sql('show tables').df()['name'])
        if 'data' in code_list:
            con.execute('drop table data')
        code_list = list(con.sql('show tables').df()['name'])

    if target == 'content':
        re_dict['content'] = con.sql('show tables').df()
    else:
        if field != '*':
            field = ','.join(field)
        
        for code in code_list:
            sql_string = f"select {field} from '{code}'"
            if bool(start) or bool(end):
                sql_string = sql_string + ' where'
            if bool(start):
                sql_string = sql_string + f" date >= '{start}'"
            if bool(end):
                sql_string = sql_string + f" and date <= '{end}'"

            re_dict[code] = \
                con.sql(sql_string).df().fillna(np.NaN)
            
    return re_dict

if __name__ == '__main__':
    re_dict = stock_data("/root/autodl-tmp/data",["002028.SZ","002030.SZ","002031.SZ"])
    print(re_dict)

