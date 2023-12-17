from db_init import *
db = SessionLocal()
"""
uers
"""
def show_users():
    # Fetch all users
    all_users = db.query(User).all()

    # Print user details with aligned columns
    print("{:<8} {:<20} {:<20} {:<20} {:<20}".format("ID", "Username", "Password", "Category", "Permission"))
    print("-" * 80)
    for user in all_users:
        print("{:<8} {:<20} {:<20} {:<20} {:<20}".format(user.id, user.username, user.password, user.user_category,
                                                         user.user_permissions))

def add_user(username=None, password=None,user_category=None,user_permissions = None):
    assert username and password and user_category and user_permissions,"information missing，please give the all infomations"
    new_user = User(username=username, password=password, user_category=user_category,user_permissions=user_permissions)
    db.add(new_user)
    db.commit()
def update_user(username=None,new_password=None,new_user_category=None,new_user_permissions = None):
    """ username 不可改"""
    assert username,"please give the username"
    assert new_password or new_user_category or new_user_permissions,"information missing，please give info to be change"
    user_to_update = db.query(User).filter(User.username ==username).first()
    if new_password:
        user_to_update.password = new_password
    if new_user_category:
        user_to_update.user_category = new_user_category
    if new_user_permissions:
        user_to_update.user_permissions = new_user_permissions
    db.commit()

def delete_user(username:str):

    # 1. 删除与该用户相关的 AccessLog 和 RequestLog
    db.query(AccessLog).filter(AccessLog.username == username).delete()
    db.query(RequestLog).filter(RequestLog.username == username).delete()
    # 2. 删除该用户
    db.query(User).filter(User.username == username).delete()
    # 3. 提交事务
    db.commit()

"""
user_permissions
"""
def show_permisssions():
    all_permissions = db.query(UserPermission).all()
    print("{:<8} {:<20} {:<20} {:<20} ".format("ID", "Permission", "max_Length", "max_Range"))
    print("-" * 80)
    for i in all_permissions:
        print("{:<8} {:<20} {:<20} {:<20}".format(i.id, i.user_permission, i.max_data_length, i.max_data_range))

def add_permission(user_permission=None,max_data_length=None,max_data_range=None):
    assert user_permission and max_data_length and max_data_range,"information missing，please give the all infomations"
    permission = UserPermission(user_permission = user_permission,max_data_length = max_data_length,max_data_range=max_data_range)
    db.add(permission)
    db.commit()
def update_permission(user_permission=None,new_max_data_length=None,new_max_data_range=None):
    """ user_permission 不可改"""
    assert user_permission,"please give the user_permission"
    assert new_max_data_length or new_max_data_range,"information missing，please give info to be change"
    user_to_update = db.query(UserPermission).filter(UserPermission.user_permission == user_permission).first()

    if new_max_data_length:
        user_to_update.max_data_length = new_max_data_length
    if new_max_data_range:
        user_to_update.max_data_range = new_max_data_range
    db.commit()
def delete_user(user_permission):

    # 1. 删除与该用户相关的 AccessLog 和 RequestLog
    db.query(User).filter(User.permission == user_permission).delete()
    # 2. 删除该用户
    db.query(UserPermission).filter(UserPermission.user_permission == user_permission).delete()
    # 3. 提交事务
    db.commit()


"""
access_log
"""


def show_access_logs():
    all_access_logs = db.query(AccessLog).all()

    print(
        "{:<8} {:<8} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("ID", "User ID", "Code List", "Period", "Field","Start", "End", "Timestamp"))
    print("-" * 120)

    for log in all_access_logs:
        print("{:<8} {:<8} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(log.id, log.username, log.code_list,
                                                                             log.period, log.field, log.start if log.start else "*", log.end if log.end else "*",
                                                                             str(log.timestamp)))


def add_access_log(username=None, code_list="*", period="1d", field="*", start=None, end=None):
    assert username , "Information missing, please provide all required information"
    access_log = AccessLog(username=username, code_list=code_list, period=period, field=field, start=start, end=end)
    db.add(access_log)
    db.commit()

def delete_access_log(log_id=None):
    assert log_id, "Please provide the log ID"
    db.query(AccessLog).filter(AccessLog.id == log_id).delete()
    db.commit()

"""
"""
# Fetch all request logs
def show_request_logs():
    all_request_logs = db.query(RequestLog).all()
    print("{:<8} {:<10} {:<20} {:<20} {:<20} {:<20} {:<20}".format("ID", "User ID", "Code List", "Period", "Field", "Start", "End"))
    print("-" * 120)
    for log in all_request_logs:
        print("{:<8} {:<10} {:<20} {:<20} {:<20} {:<20} {:<20}".format(
            log.id, log.username, log.code_list, log.period, log.field, log.start, log.end
        ))

# Add a new request log
def add_request_log(username, code_list="*", period="1d", field="*", start=None, end=None):
    assert username, "Information missing, please provide all required information"
    request_log = RequestLog(username=username, code_list=code_list, period=period, field=field, start=start, end=end)
    db.add(request_log)
    db.commit()


# Delete a request log
def delete_request_log(log_id):
    assert log_id, "Please provide the log ID"
    db.query(RequestLog).filter(RequestLog.id == log_id).delete()
    db.commit()

if __name__ == '__main__':

    show_users()
    # add_user('zhangwj',123456,'intern','level3')
    # add_user('luqf',123456,'intern','level3')
    # show_users()
    # add_permission('level1',20000,2000)
    # add_permission('level2',40000,4000)
    # add_permission('level3',100000,10000)
    # show_permisssions()
    # show_access_logs()
    # show_users()