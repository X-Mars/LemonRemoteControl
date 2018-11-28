from django.shortcuts import render
from Zabbix.master import ZabbixMaster
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from weChat.authenticate import login_check, GetUserToken, decode_jwt, GetUserInfo

# Create your views here.


def login(request):
    if(request.method == 'GET'):
        code = request.GET.get('code', None)
        if code:
            G = GetUserToken()
            token = G.get_user_info(code=code)
            if token:
                response = HttpResponseRedirect('/')
                response.set_cookie('token', token)
                return response
            else:
                data = {
                    'status': 'error',
                    'msg': '您没有权限访问，请联系管理员！'
                }
                return JsonResponse(data=data)
        else:
            data = {
                'status': 'error',
                'msg': '请使用企业微信打开！'
            }
            return JsonResponse(data=data)

@login_check
def index(request):
    if(request.method == 'GET'):
        token = request.COOKIES.get('token')
        G = GetUserInfo()
        user_info = G.get_user_info(token=token)
        return render(request, 'index.html', user_info)
