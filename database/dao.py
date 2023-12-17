from pydantic import BaseModel

class DataRequest(BaseModel):
    user_name: str
    pwd:str
    code_list: str = "*"
    period: str = "1d"
    field: str = "*"
    start: str = None
    end: str = None
