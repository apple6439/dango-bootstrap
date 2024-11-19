from django.shortcuts import render, HttpResponse

# Create your views here.

'''
首页
'''


def home(request):
    return render(request, 'home.html')


'''
员工管理
'''


def user_list(request):
    return render(request, 'user_list.html')


'''
部门管理
'''


def department_list(request):
    return render(request, 'department_list.html')


'''
订单管理
'''


def order_list(request):
    return render(request, 'order_list.html')
