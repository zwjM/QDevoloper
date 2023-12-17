'''
Author: zhangwj
Date: 2023-12-09
Description: 创建数据库（用于记录用户信息和行为信息）
'''

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from tools import get_nowtime_beijing

# 配置数据库连接
DATABASE_URL = "sqlite:///./quant.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库（如果数据库不存在）
Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_category = Column(String, nullable=False)
    user_permissions = Column(String, ForeignKey("user_permissions.user_permission"))


    permission = relationship("UserPermission", back_populates="users")
    access_logs = relationship("AccessLog", back_populates="users")
    request_logs = relationship("RequestLog", back_populates="users")

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_permission = Column(String, nullable=False, unique=True)  # Assuming user categories are unique
    max_data_length = Column(Integer, nullable=False)
    max_data_range = Column(String, nullable=False)
    users = relationship("User", back_populates="permission")
class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(Integer, ForeignKey("users.username"), nullable=False)
    code_list = Column(String, default="*")
    period = Column(String, default="1d")
    field = Column(String, default="*")
    start = Column(String, nullable=True)
    end = Column(String, nullable=True)
    timestamp = Column(DateTime, default=get_nowtime_beijing())

    users = relationship("User", back_populates="access_logs")
class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(Integer, ForeignKey("users.username"), nullable=False)
    code_list = Column(String, default="*")
    period = Column(String, default="1d")
    field = Column(String, default="*")
    start = Column(String,nullable=True)
    end = Column(String, nullable=True)
    status = Column(String,nullable=True)
    timestamp = Column(DateTime, default=get_nowtime_beijing())

    users = relationship("User", back_populates="request_logs")

# 创建所有需要的表单（如果不存在）
Base.metadata.create_all(bind=engine)