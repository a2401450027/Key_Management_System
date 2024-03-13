from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
'''

'''
class AuthMid(MiddlewareMixin):
    def process_request(self,request):
        #排除不需要登录就能访问的页面
        if request.path_info in ["/login/","/register/","/get_userinfo/"]:
            return
        #读取session信息
        info = request.session.get('info')
        if info:
            return
        return redirect('/login/')

