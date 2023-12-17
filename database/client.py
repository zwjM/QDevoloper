import requests
import json
from parse import *
url = "http://127.0.0.1:8000/get_data/"
def get_raw_data(user_name:str,pwd:str,code_list: list= "*",period: str='1d', start: str='', end: str='', field: list='*'):
    data = {
        "user_name": user_name,
        "pwd":pwd,
        "code_list":json.dumps(code_list),
        "period": period,
        "field": json.dumps(field),
        "start":start,
        "end":end
    }

    response = requests.post(url, headers=data,json = data)
    print(response.headers)
    print(response.status_code)
    # print(parse_response(response))
if __name__ == '__main__':
    get_raw_data("zhangwj",'123456',["002028.SZ","002030.SZ","002031.SZ"],period='1d',field=["date","open","high"],start="2023-01-01",end="2023-01-15")