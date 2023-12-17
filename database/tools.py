import os.path
from datetime import datetime
import pytz
import pandas as pd
def get_nowtime_beijing():
    # 设置时区为北京时区
    beijing_timezone = pytz.timezone('Asia/Shanghai')
    # 获取当前时间（UTC时间）
    utc_now = datetime.utcnow()
    # 将 UTC 时间转换为北京时间
    beijing_now = utc_now.replace(tzinfo=pytz.utc).astimezone(beijing_timezone)
    return beijing_now

def splite_field2df(re_dict,outputdir='./'):
    feature_list = re_dict[list(re_dict.keys())[0]].columns.drop('date')
    my_dict = dict()
    for fea in feature_list:
        my_dict[fea] = []

    for k,v in re_dict.items():
        v = v.set_index('date')
        for fea in feature_list:
            my_dict[fea].append(v[fea].rename(k))
    for k,v in my_dict.items():
        pd.concat(v,axis=1).to_csv(os.path.join(outputdir,f'{k}.dat'), index=True)

