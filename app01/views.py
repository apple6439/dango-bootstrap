from django import forms
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from app01.models import Department, Employee, Order, Admin
from django.core.paginator import Paginator
import os

# Create your views here.
'''
登录页面
'''


def index(request):
    return render(request, 'index.html')


'''
首页
'''


def home(request):
    return render(request, 'home.html')


'''
员工管理
'''


class UserModelForm(forms.ModelForm):
    class Meta:
        model = Employee
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


def user_list(request):
    form = UserModelForm()
    # 查找功能,通过url来查询
    data_dict = {}
    # 这个.get('q','')是字典的一个方法，作用是当尝试获取key为q的value是，不存在q是返回空串
    username = request.GET.get('username', '')
    gender = request.GET.get('gender', '')
    # 查询的结果存在时
    if username or gender:
        # 使用 icontains 进行模糊匹配
        if username:
            data_dict['name__icontains'] = username
        if gender:
            if gender == 'male':
                gender = 0
            elif gender == 'female':
                gender = 1
            data_dict['gender'] = gender
    print(data_dict)
    res = Employee.objects.filter(**data_dict)
    print("查询结果{}".format(res))
    # # -字段名 是desc降序
    data__list = Employee.objects.filter(**data_dict)
    # 分页功能
    paginator = Paginator(data__list, 5)  # 每页有5条数据
    current_page = int(request.GET.get('page', 1))  # 获取当前页码,方便前端渲染已选择的页面，例如添加active
    user_page = paginator.page(current_page)  # 当前的页码,并且生成这一个页码的数据

    return render(request, 'user_list.html', {
        'form': form,
        # 'departments': data__list,
        # 'search_data': value,
        'user_page': user_page,
        'paginator': paginator,
        'current_page': current_page, })
    # return render(request, 'department_list.html',
    #               {'departments_parent': departments_parent, 'departments': departments})


@csrf_exempt
def user_add(request):
    form = UserModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def user_update(request, nid):
    if request.method == 'GET':
        row_dict = Employee.objects.filter(employee_id=nid).values('name', 'gender', 'hire_date',
                                                                   'salary',
                                                                   'department').first()
        print(row_dict)
        if row_dict:
            # 格式化 hire_date 字段
            if row_dict['hire_date']:
                row_dict['hire_date'] = row_dict['hire_date'].strftime('%Y-%m-%d')
            return JsonResponse({'status': True, 'data': row_dict})
    else:
        row_object = Employee.objects.filter(employee_id=nid).first()
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True, 'error': form.errors}
            return JsonResponse(data_dict)
        else:
            data_dict = {'status': False, 'error': form.errors}
            return JsonResponse(data_dict)


@csrf_exempt
def user_delete(request, nid):
    # 单行删除
    if request.method == 'GET':
        Employee.objects.filter(employee_id=nid).delete()
        return JsonResponse({'status': True})
    # 多行删除
    else:
        # 获取前台返回过来的列表
        nids = request.POST.getlist('nids[]')
        print(nids)
        if not nids:
            return JsonResponse({'status': True, 'error': '删除数据为空'})
        else:
            # 字段名__in 若 department_id in nids，则进行后面的逻辑操作
            Employee.objects.filter(employee_id__in=nids).delete()
        return JsonResponse({'status': True})


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
    # 单行删除
    if request.method == 'GET':
        Department.objects.filter(department_id=nid).delete()
        return JsonResponse({'status': True})
    # 多行删除
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


@csrf_exempt
def department_update(request, nid):
    if request.method == 'GET':
        row_dict = Department.objects.filter(department_id=nid).values('name', 'manager', 'parent_department',
                                                                       'created_at',
                                                                       'performance').first()
        # Department.objects.filter(department_id=nid).update()
        print(row_dict)
        if row_dict:
            # 格式化 created_at 字段
            if row_dict['created_at']:
                row_dict['created_at'] = row_dict['created_at'].strftime('%Y-%m-%d')
            return JsonResponse({'status': True, 'data': row_dict})
    else:
        row_object = Department.objects.filter(department_id=nid).first()
        form = DepartmentModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            data_dict = {'status': True, 'error': form.errors}
            return JsonResponse(data_dict)
        else:
            data_dict = {'status': False, 'error': form.errors}
            return JsonResponse(data_dict)


'''
订单管理
'''


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, field in self.fields.items():
            # 字段中有属性保留原来的属性，没有才添加
            if k != 'product_image':
                if field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
                    field.widget.attrs['placeholder'] = field.label
                else:
                    field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def order_list(request):
    form = OrderModelForm()
    # 查找功能,通过url来查询
    data_dict = {}
    # 这个.get('q','')是字典的一个方法，作用是当尝试获取key为q的value是，不存在q是返回空串
    value = request.GET.get('q', '')
    # 查询的结果存在时
    if value:
        # 使用 icontains 进行模糊匹配
        data_dict['product_name__icontains'] = value
    # res = PrettyNum.objects.filter(mobile__contains=value)
    # res = PrettyNum.objects.filter(**data_dict)
    # print(res)
    # -字段名 是desc降序
    data__list = Order.objects.filter(**data_dict)
    # 分页功能
    paginator = Paginator(data__list, 5)  # 每页有5条数据
    current_page = int(request.GET.get('page', 1))  # 获取当前页码,方便前端渲染已选择的页面，例如添加active
    user_page = paginator.page(current_page)  # 当前的页码,并且生成这一个页码的数据

    return render(request, 'order_list.html', {
        'form': form,
        'user_page': user_page,
        'paginator': paginator,
        'current_page': current_page, })


@csrf_exempt
def order_add(request):
    if request.method == 'POST':
        form = OrderModelForm(data=request.POST, files=request.FILES)
        # print(request.POST)
        # print(request.FILES.get('product_image'))
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def order_delete(request, nid):
    # 单行删除
    if request.method == 'GET':
        orders = Order.objects.filter(order_id=nid).first()
        img_path = orders.product_image.path
        if img_path:
            os.remove(img_path)
            Order.objects.filter(order_id=nid).delete()
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': True, 'error': '记录不存在'})
    # 多行删除
    else:
        # 获取前台返回过来的列表
        nids = request.POST.getlist('nids[]')
        print(nids)
        if not nids:
            return JsonResponse({'status': True, 'error': '删除数据为空'})
        else:
            # 字段名__in 若 department_id in nids，则进行后面的逻辑操作
            orders = Order.objects.filter(order_id__in=nids)
            for order in orders:
                img_path = order.product_image.path
                if img_path:
                    os.remove(img_path)
                    Order.objects.filter(order_id=nid).delete()
                else:
                    return JsonResponse({'status': True, 'error': '记录不存在'})

            # 字段名__in 若 department_id in nids，则进行后面的逻辑操作
            Order.objects.filter(order_id__in=nids).delete()
            return JsonResponse({'status': True})


@csrf_exempt
def order_update(request, nid):
    if request.method == 'GET':
        row_dict = Order.objects.filter(order_id=nid).values('product_image', 'product_name', 'order_date',
                                                             'quantity',
                                                             'customer_name').first()
        print(row_dict)
        if row_dict:
            # 格式化 created_at 字段
            if row_dict['order_date']:
                row_dict['order_date'] = row_dict['order_date'].strftime('%Y-%m-%d %H:%M')
            return JsonResponse({'status': True, 'data': row_dict})
    else:
        row_object = Order.objects.filter(order_id=nid).first()
        form = OrderModelForm(data=request.POST, instance=row_object, files=request.FILES)
        if form.is_valid():
            img = form.cleaned_data['product_image']
            print(img)

            # 判断media中是否存在相同，有则删除
            file_path = os.path.join(settings.MEDIA_ROOT, 'product_images', img.name)  # img.name 用于获取文件名
            print(file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            form.save()
            data_dict = {'status': True, 'error': form.errors}
            return JsonResponse(data_dict)
        else:
            data_dict = {'status': False, 'error': form.errors}
            return JsonResponse(data_dict)


'''
管理员
'''


def admin_info(request):
    return render(request, 'admin_info.html')
