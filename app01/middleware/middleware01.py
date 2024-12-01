# 中间件统一处理用户登录的验证
# 应用中间件还要去setting中去设置
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, render
from django.urls import path


class LoginMiddleware(MiddlewareMixin):
    """中间件1"""

    # 读取当前访问用户的session信息，如果不为空，则说明已登录
    def process_request(self, request):
        # 排除哪些不需要登录就能访问的页面，如login
        if request.path_info in ['/login/']:
            return
        info = request.session.get('info')
        # 已登录
        if info:
            return
        # 未登录
        else:
            # return HttpResponse('123')
            return redirect('/login/')

    def process_response(self, request, response):
        return response
