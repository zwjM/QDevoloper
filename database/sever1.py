from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
# from typing import List

from data import *
import pickle
import json

from parse import *
from fastapi.middleware.cors import CORSMiddleware
from ProcessMiddleWare import *
from ProcessASGIMiddleWare import *
import logging
from starlette.responses import Response
from db_init import *
from dao import *
logging.basicConfig(level=logging.INFO)

app = FastAPI()
# app.add_middleware(ProcessMiddleware,header_namespace="middleware")

app.add_middleware(ProcessAuthorityASGIMiddleware,header_namespace="middleware")
app.add_middleware(ProcessLogsASGIMiddleware,header_namespace="middleware")
# Data model for receiving client's data request

class QSever:
    def __init__(self):
        pass

# Data processing function to receive data requests and record access logs
@app.post("/get_data/")
async def get_data(data_request: DataRequest,request: Request,response: Response):
    logging.info("    Received a request on the root endpoint")

    # re_dict = stock_data(path="",code_list=data_request.code_list,period=data_request.period,start=data_request.start,end=data_request.end,field=data_request.field)
    # print(json.loads(data_request.code_list))
    # print(type(json.loads(data_request.code_list)))

    # Add your data retrieval logic here; this is a simple example returning a response
    # response_data = {"message": "Data retrieval successful", "data": {"code_list": data_request.code_list}}
    headers = dict(request.scope['headers'])
    print('Svr:',headers[b'authority'])
    if headers[b'authority']=="no":
        raise HTTPException(status_code=404, detail="Check your authority,permission refused")

    with open("test.pkl", "rb") as pickle_file:
        response_data = pickle.load(pickle_file)
    response_data = parse_to_jsonabel(response_data)
    # return JSONResponse(content=response_data)
    return JSONResponse(json.dumps(response_data))



# Run FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='sever1:app', host="127.0.0.1", port=8000, reload=True)
