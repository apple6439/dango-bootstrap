from django import forms
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Department
from django.core.paginator import Paginator

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


class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 字段中有属性保留原来的属性，没有才添加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def department_list(request):
    form = DepartmentModelForm()
    departments_parent = Department.objects.filter(parent_department=None)  # 获取顶级部门
    # 查找功能,通过url来查询
    data_dict = {}
    # 这个.get('q','')是字典的一个方法，作用是当尝试获取key为q的value是，不存在q是返回空串
    value = request.GET.get('q', '')
    # 查询的结果存在时
    if value:
        # 使用 icontains 进行模糊匹配
        data_dict['name__icontains'] = value
    # res = PrettyNum.objects.filter(mobile__contains=value)
    # res = PrettyNum.objects.filter(**data_dict)
    # print(res)
    # -字段名 是desc降序
    data__list = Department.objects.filter(**data_dict)
    # 分页功能
    paginator = Paginator(data__list, 5)  # 每页有5条数据
    current_page = int(request.GET.get('page', 1))  # 获取当前页码,方便前端渲染已选择的页面，例如添加active
    user_page = paginator.page(current_page)  # 当前的页码,并且生成这一个页码的数据

    return render(request, 'department_list.html', {
        'form': form,
        'departments_parent': departments_parent,
        'departments': data__list,
        'search_data': value,
        'user_page': user_page,
        'paginator': paginator,
        'current_page': current_page, })
    # return render(request, 'department_list.html',
    #               {'departments_parent': departments_parent, 'departments': departments})


@csrf_exempt
def department_add(request):
    form = DepartmentModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def department_delete(request, nid):
    if request.method == 'GET':
        Department.objects.filter(department_id=nid).delete()
        return JsonResponse({'status': True})
    else:
        # 获取前台返回过来的列表
        nids = request.POST.getlist('nids[]')
        print(nids)
        if not nids:
            return JsonResponse({'status': True, 'error': '删除数据为空'})
        else:
            # 字段名__in 若 department_id in nids，则进行后面的逻辑操作
            Department.objects.filter(department_id__in=nids).delete()
        return JsonResponse({'status': True})


'''
订单管理
'''


def order_list(request):
    return render(request, 'order_list.html')
