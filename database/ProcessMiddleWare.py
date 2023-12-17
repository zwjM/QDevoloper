import time
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import json
from datetime import datetime
import copy
class ProcessMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_namespace: str):
        super().__init__(app)
        # 自定义参数，用于定义middleware的header名称空间
        self.header_namespace = header_namespace

    async def dispatch(self, request: Request, call_next):
        # 接收来自客户端的Request请求；
        headers = dict(request.scope['headers'])
        print(request.scope)

        # # 定义middleware开始时间
        # middleware_start_time = _time2str(datetime.now())
        # # 将middleware开始时间添加到request的headers中，这里request.headers是一个可读可写的对象，但是它的值是不可变的，所以这里需要将request.headers转换为字典，然后再修改字典的值，最后再将字典转换为元组，赋值给request.scope['headers']；
        # headers[b'middleware_start_time'] = middleware_start_time.encode('utf-8')
        # request.scope['headers'] = [(k, v) for k, v in headers.items()]
        # 将Request请求传回原路由
        response = await call_next(request)
        print(2)
        # # 为了更好的观察middleware的执行过程，这里让middleware休眠1秒钟
        # time.sleep(1)
        #
        # # 接收来自原路由的Response响应，将middleware结束时间添加到response的headers中
        # response.headers[f"{self.header_namespace}_start_time"] = middleware_start_time
        # response.headers[f"{self.header_namespace}_end_time"] = _time2str(datetime.now())

        return response
