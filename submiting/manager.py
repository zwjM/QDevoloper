import time

class Manager:
    def __init__(self, api_key, api_pass, max_quota):
        self.api_key = api_key
        self.api_pass = api_pass
        self.max_quota = max_quota
        self.current_quota = 0
        self.log = []

    def authenticate(self, user_key, user_pass):
        return user_key == self.api_key and user_pass == self.api_pass

    def request_data(self, user_key, user_pass, data_amount):
        if not self.authenticate(user_key, user_pass):
            return "Authentication failed. Access denied."

        if self.current_quota + data_amount > self.max_quota:
            return "Quota exceeded. Please submit a request for additional quota."

        self.current_quota += data_amount
        self.log.append({"user_key": user_key, "timestamp": time.time(), "data_amount": data_amount})
        return f"Data request successful. Current quota: {self.current_quota}/{self.max_quota}."

    def submit_quota_request(self, user_key, user_pass, additional_quota):
        if not self.authenticate(user_key, user_pass):
            return "Authentication failed. Access denied."

        # Assuming there's some approval process for quota requests.
        # You can extend this part based on your specific requirements.
        # For simplicity, we'll just add the requested quota directly.
        self.max_quota += additional_quota
        return f"Quota request submitted. New maximum quota: {self.max_quota}."

    def view_log(self, user_key, user_pass):
        if not self.authenticate(user_key, user_pass):
            return "Authentication failed. Access denied."

        return self.log

# 示例用法
data_manager = Manager(api_key="your_api_key", api_pass="your_api_pass", max_quota=1000)

# 用户访问数据
response = data_manager.request_data(user_key="user_key_1", user_pass="user_pass_1", data_amount=200)
print(response)

# 用户提交额外的配额请求
response = data_manager.submit_quota_request(user_key="user_key_1", user_pass="user_pass_1", additional_quota=500)
print(response)

# 用户查看访问日志
log = data_manager.view_log(user_key="user_key_1", user_pass="user_pass_1")
print(log)
