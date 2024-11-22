from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from app01.models import Department
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
    departments = Department.objects.filter(parent_department=None)  # 获取顶级部门
    return render(request, 'department_list.html', {'departments': departments})


def get_department_info(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    manager_username = department.manager.name if department.manager else None
    parent_department_name = department.parent_department.name if department.parent_department else None

    res = {
        'department': {
            'department_id': department.department_id,
            'name': department.name,
            'manager': manager_username,
            'parent_department': parent_department_name,
            'created_at': department.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'performance': department.performance,
        }
    }
    return JsonResponse(res)

'''
订单管理
'''


def order_list(request):
    return render(request, 'order_list.html')
