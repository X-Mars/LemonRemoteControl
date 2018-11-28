from django.http import JsonResponse
# from weChat.models import WeChat
import requests, jwt, json, time
from Lemon.settings import SECRET_KEY, WECHAT_SETTING

def make_jwt(data):
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

class BaseWeChat(object):
    def __init__(self):
        # wechat_info = WeChat.objects.all().values()[0]
        print(WECHAT_SETTING)
        self.corp_id = WECHAT_SETTING['corp_id']
        self.secret = WECHAT_SETTING['secret']
        self.agent_id = WECHAT_SETTING['agent_id']
        self.tag_id = WECHAT_SETTING['tag_id']
        self.session = requests.session()
        self.token = self.get_token()

    def get_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" %(self.corp_id, self.secret)
        r = self.session.get(url=url)
        print(r.json())
        return r.json()['access_token']

class GetUserToken(BaseWeChat):

    def get_party_user(self, party_id):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=%s&department_id=%s&fetch_child=1" %(self.token, party_id)
        r = self.session.get(url=url)
        print(r.json())
        return r.json()['userlist']

    def get_tag_user(self, user_id):
        url = "https://qyapi.weixin.qq.com/cgi-bin/tag/get?access_token=%s&tagid=%s" %(self.token, self.tag_id)
        r = self.session.get(url=url)
        print(r.json())
        for user_info in r.json()['userlist']:
            if user_info['userid'] == user_id:
                return True
        for party_id in r.json()['partylist']:
            user_list = self.get_party_user(party_id=party_id)
            for user_info in user_list:
                if user_info['userid'] == user_id:
                    return True
        return False

    def get_user_info(self, code):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s" %(self.token, code)
        r = self.session.get(url=url).json()
        print(r)
        user_id = r['UserId']
        user_status = self.get_tag_user(user_id=user_id)
        if user_status:
            # r.pop('user_ticket')
            expires_in = r['expires_in'] - 20 + int(time.time())
            r['expires_in'] = expires_in
            print(r)
            token = make_jwt(r)
            print(token)
            return token.decode('utf-8')

        return user_status

class GetUserInfo(BaseWeChat):

    def get_user_info(self, token):
        token_info = decode_jwt(token.encode())
        print("=================================")
        print(token_info)
        user_id = token_info['UserId']
        print(user_id)
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s&userid=%s" %(self.get_token(), user_id)
        print(url)

        r = self.session.get(url=url)
        print(r.json())
        data = r.json()
        avatar = data['avatar']
        data['avatar'] = (avatar.replace('/0', '/100'))
        print("=================================")

        return data

def login_check(func):
    '''身份认证装饰器，
    :param func:
    :return:
    '''
    def wrapper(request,*args,**kwargs):
        print('here')
        print(request.COOKIES)
        token = request.COOKIES.get('token')
        if not token:
            data = {
                'status': 'error',
                'msg': '请您先登录！'
            }
            return JsonResponse(data=data)
        else:
            token_info = decode_jwt(token.encode())
            time_now = int(time.time())
            if token_info['expires_in'] < time_now:
                data = {
                    'status': 'error',
                    'msg': '登陆过期，请重新登陆！'
                }
                return JsonResponse(data=data)

        return func(request,*args, **kwargs)
    return wrapper

