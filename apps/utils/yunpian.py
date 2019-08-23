
import json,requests
class YunPian(object):
    def init(self,api_key):
        self.api_key=api_key
        self.signle_url='https://sms.yunpian.com/v2/sms/single_send.json'


    def send_sms(self,code,mobile):
        parmsa={
            "api_key":self.api_key,
            "mobile":mobile,
            "code":"【文兆庆的生鲜超市】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response=requests.post(self.signle_url,parmsa)
        re_dict = json.loads(response.text)
        return re_dict
