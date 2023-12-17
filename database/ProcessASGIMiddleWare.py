import time
from datetime import datetime
from fastapi import Request

from db_control import *
from dao import *

class ProcessAuthorityASGIMiddleware:
    def __init__(self, app, header_namespace: str):
        self.app = app
        # 自定义参数，用于定义middleware的header名称空间
        self.header_namespace = header_namespace

    # ASGI 中间件必须是接受三个参数的可调用对象，即 scope、receive、send；
    async def __call__(self, scope, receive, send):

        request = Request(scope)

        headers = dict(request.scope['headers'])

        user_name = headers[b'user_name'].decode('utf-8')
        pwd = headers[b'pwd'].decode('utf-8')
        authority = self.check(user_name,pwd)
        print(authority)
        # 定义middleware开始时间
        headers[b'authority'] = authority
        request.scope['headers'] = [(k, v) for k, v in headers.items()]

        # 定义Send函数，用于将middleware开始时间和middleware结束时间添加到response的headers中
        async def add_headers(message):
            # if message["type"] == "http.response.start":
                # new_headers = MutableHeaders(scope=message)
                # new_headers.append(f"{self.header_namespace}_start_time", "11111")
                # new_headers.append(f"{self.header_namespace}_end_time", "222222")
            await send(message)

        # 将scope、receive、add_headers传递给原始的ASGI应用程序
        return await self.app(scope, receive, add_headers)

    def check(self,user_name, pwd):
        # 根据user_id 和密码进行权限审核。
        user_x = db.query(User).filter(User.username == user_name).first()
        if not user_x:
            print("username not exits！")
            return "no"
        pwd_x = user_x.password
        if pwd_x != pwd:
            print("pwd is not correct！")
            return "no"
        return "yes"


class ProcessLogsASGIMiddleware:
    def __init__(self, app, header_namespace: str):
        self.app = app
        # 自定义参数，用于定义middleware的header名称空间
        self.header_namespace = header_namespace

    # ASGI 中间件必须是接受三个参数的可调用对象，即 scope、receive、send；
    async def __call__(self, scope, receive, send):

        request = Request(scope)
        headers = dict(request.scope['headers'])

        user_name = headers[b'user_name'].decode('utf-8')
        pwd = headers[b'pwd'].decode('utf-8')
        code_list = headers[b'code_list'].decode('utf-8')
        period = headers[b'period'].decode('utf-8')
        field = headers[b'field'].decode('utf-8')
        start =  headers[b'start'].decode('utf-8')
        end = headers[b'end'].decode('utf-8')
        self.writedown_request(user_name,code_list,period,field,start,end)

        request.scope['headers'] = [(k, v) for k, v in headers.items()]

        # 定义Send函数，用于将middleware开始时间和middleware结束时间添加到response的headers中
        async def add_headers(message):
            # if message["type"] == "http.response.start":
            #     new_headers = MutableHeaders(scope=message)
            #     new_headers.append(f"{self.header_namespace}_start_time", "11111")
            #     new_headers.append(f"{self.header_namespace}_end_time", "222222")
            await send(message)

        # 将scope、receive、add_headers传递给原始的ASGI应用程序
        return await self.app(scope, receive, add_headers)


    def writedown_request(self,username,code_list,period,field,start,end):
        assert username, "Information missing, please provide all required information"
        add_access_log(
            username=username,
            code_list=code_list,
            period=period,
            field=field,
            start=start,
            end=end
        )
