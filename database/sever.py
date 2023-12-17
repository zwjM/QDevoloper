from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
# from typing import List
from pydantic import BaseModel
from data import *
import pickle
import json
from db_control import *
from parse import *
app = FastAPI()
import logging
logging.basicConfig(level=logging.INFO)

# Data model for receiving client's data request
class DataRequest(BaseModel):
    user_id: int
    pwd:str
    code_list: str = "*"
    period: str = "1d"
    field: str = "*"
    start: str = None
    end: str = None

def check(user_id,pwd):
    # 根据user_id 和密码进行权限审核。
    user_x = db.query(User).filter(User.id == user_id).first()
    if not user_x:
        print("user_id not exits！")
        return False
    pwd_x = user_x.password
    user_name_x = user_x.username
    if pwd_x!=pwd:
        print("pwd is not correct！")
        return False
    return True

# Data processing function to receive data requests and record access logs
@app.post("/get_data/")
async def get_data(data_request: DataRequest):
    logging.info("    Received a request on the root endpoint")
    # Record access log
    add_access_log( user_id=data_request.user_id,
        code_list=data_request.code_list,
        period=data_request.period,
        field=data_request.field,
        start=data_request.start,
        end=data_request.end)

    # permission checks based on user_id
    if not check(data_request.user_id,data_request.pwd):
        return HTTPException(status_code=404, detail="permission refused")


    # re_dict = stock_data(path="",code_list=data_request.code_list,period=data_request.period,start=data_request.start,end=data_request.end,field=data_request.field)
    # print(json.loads(data_request.code_list))
    # print(type(json.loads(data_request.code_list)))

    # Add your data retrieval logic here; this is a simple example returning a response
    # response_data = {"message": "Data retrieval successful", "data": {"code_list": data_request.code_list}}
    with open("test.pkl", "rb") as pickle_file:
        response_data = pickle.load(pickle_file)
    response_data = parse_to_jsonabel(response_data)
    # return JSONResponse(content=response_data)
    return JSONResponse(json.dumps(response_data))



# Run FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
