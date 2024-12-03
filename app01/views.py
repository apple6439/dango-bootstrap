from django import forms
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from app01.models import Department, Employee, Order, Admin
from django.core.paginator import Paginator
import os
from django.db import models

# Create your views here.
'''
404页面
'''


def page_not_found(request, exception):
    return render(request, '404.html')


'''
500页面
'''


def page_error(request):
    return render(request, '500.html')


'''
登录页面
'''


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'password']
        widgets = {
            # render_value=True错误时保留
            'password': forms.PasswordInput(render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 字段中有属性保留原来的属性，没有才添加
            if field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'placeholder': field.label}


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(label='密码', required=True,
                               widget=forms.PasswordInput(attrs={"autocomplete": 'off'}))
    confirm_password = forms.CharField(label='确认密码', required=True,
                                       widget=forms.PasswordInput(attrs={"autocomplete": 'off'}))

    class Meta:
        model = Admin
        fields = ['email', 'name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 字段中有属性保留原来的属性，没有才添加
            if field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'placeholder': field.label}


def login(request):
    if request.method == 'GET':
        login_form = LoginModelForm()
        return render(request, 'index.html', {'login_form': login_form, 'register_form': RegisterModelForm()})

    elif request.method == 'POST':
        login_form = LoginModelForm(request.POST)
        if login_form.is_valid():
            print(login_form.cleaned_data)
            information = login_form.cleaned_data
            row_object = Admin.objects.filter(**information).first()
            admin_image_dict = Admin.objects.filter(**information).values('admin_image').first()
            admin_image = admin_image_dict['admin_image']
            if row_object:
                # 成功后进行如下处理，cookie和session
                # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session,django中已经帮程序员实现，我们只需要传入登陆者的信息就行
                request.session['info'] = {'id': row_object.admin_id, 'name': row_object.name,
                                           'email': row_object.email,
                                           'admin_image': admin_image}
                # 这里我们超时时间重新设置一下,这里我设置信息可以保存七天，即七天之内可以不需要登录
                request.session.set_expiry(60 * 60 * 24 * 7)
                for k, v in request.session.items():
                    print(f'{k}的值为{v}')
                return redirect('/home/')
            else:
                login_form.add_error('password', '用户名或密码错误')
                return render(request, 'index.html', {'login_form': login_form})
        else:
            return render(request, 'index.html', {'login_form': login_form})


def register(request):
    if request.method == 'GET':
        register_form = RegisterModelForm()
        return render(request, 'index.html', {'login_form': LoginModelForm(), 'register_form': register_form})
    else:
        register_form = RegisterModelForm(request.POST)
        print('123')
        if register_form.is_valid():
            print(register_form.cleaned_data)
            # 判断邮箱，用户名的唯一性
            information = register_form.cleaned_data
            username = information['name']
            email = information['email']
            if Admin.objects.filter(name=username):
                register_form.add_error('name', '用户名已存在')
                return render(request, 'index.html', {'login_form': LoginModelForm(), 'register_form': register_form})
            elif Admin.objects.filter(email=email):
                register_form.add_error('email', '邮箱已注册')
                return render(request, 'index.html', {'login_form': LoginModelForm(), 'register_form': register_form})
            else:
                # 判断两次输入的密码是否相同
                password = information['password']
                confirm_password = information['confirm_password']
                if password == confirm_password:
                    # 相同则保存到数据库中去
                    register_form.save()
                    return redirect('/login/')
                else:
                    register_form.add_error('password', '两次输入的密码不一致')
                    return render(request, 'index.html',
                                  {'login_form': LoginModelForm(), 'register_form': register_form})
                pass

        else:
            return render(request, 'index.html', {'login_form': LoginModelForm(), 'register_form': register_form})


'''
首页
'''


def home(request):
    form = OrderModelForm()
    data__list = Order.objects.all()
    # 分页功能
    paginator = Paginator(data__list, 10)  # 每页有10条数据
    current_page = int(request.GET.get('page', 1))  # 获取当前页码,方便前端渲染已选择的页面，例如添加active
    user_page = paginator.page(current_page)  # 当前的页码,并且生成这一个页码的数据

    return render(request, 'home.html', {
        'user_page': user_page,
        'paginator': paginator,
        'current_page': current_page, })


def chart_data(request):
    # 获取部门业绩数据
    departments = Department.objects.values('name', 'performance')

    # 处理柱状图数据
    line_chart_data = {
        'legend': [dept['name'] for dept in departments],
        'xAxis': [dept['name'] for dept in departments],  # 部门名称
        'series': [
            {
                'name': '业绩',  # 统一的系列名称
                'data': [dept['performance'] for dept in departments]  # 所有部门的业绩
            }
        ]
    }
    # 获取员工薪资数据
    employees = Employee.objects.values('name', 'salary')
    bar_chart_data = {
        'legend': ['薪资'],
        'xAxis': [emp['name'] for emp in employees],
        'series': [
            {
                'name': '薪资',
                'data': [emp['salary'] for emp in employees]
            }
        ]
    }

    # 获取订单数量数据
    orders = Order.objects.values('product_name').annotate(total_quantity=models.Sum('quantity'))
    pie_chart_data = {
        'data': [
            {'value': order['total_quantity'], 'name': order['product_name']} for order in orders
        ]
    }

    # 返回所有数据
    return JsonResponse({
        'lineChart': line_chart_data,
        'barChart': bar_chart_data,
        'pieChart': pie_chart_data,
    })


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
        print(request.FILES)
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


class AdminAvatarModelForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['admin_image']


class AdminPasswordModelForm(forms.ModelForm):
    original_password = forms.CharField(widget=forms.PasswordInput(), label="原密码")
    password = forms.CharField(widget=forms.PasswordInput(), label="新密码")
    confirm_password = forms.CharField(label='确认密码', required=True,
                                       widget=forms.PasswordInput(attrs={"autocomplete": 'off'}))

    class Meta:
        model = Admin
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 字段中有属性保留原来的属性，没有才添加
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


# def admin_info(request):
#     if request.method == 'GET':
#         admin_id = request.session['info']['id']
#         form = AdminAvatarModelForm()
#         return render(request, 'admin_info.html', {'form': form})
#
#     elif request.method == 'POST':
#         admin_id = request.session['info']['id']
#         # 更新数据库中的用户信息
#         row_object = Admin.objects.filter(admin_id=admin_id).first()
#         form = AdminAvatarModelForm(files=request.FILES, instance=row_object)
#         if form.is_valid():
#             form.save()
#             # 更新 session 中的信息
#             print(request.session['info']['admin_image'])
#             request.session['info']['admin_image'] = ('admins/{}').format(request.FILES)
#             print(request.session['info']['admin_image'])
#
#         return redirect('/admin/info/')
def admin_info(request):
    admin_id = request.session['info']['id']
    row_object = Admin.objects.filter(admin_id=admin_id).first()
    if request.method == 'GET':
        form = AdminAvatarModelForm()
        return render(request, 'admin_info.html', {'form': form})
    else:
        print(admin_id)
        print(request.FILES)
        form = AdminAvatarModelForm(files=request.FILES, instance=row_object)
        if form.is_valid():
            # 保存表单数据,并获取保存的数据
            admin_instance = form.save()
            # 获取文件的 URL
            # uploaded_file_url = admin_instance.admin_image.url  # 绝对路径
            uploaded_file_path = admin_instance.admin_image.name  # 这会返回相对路径
            print(uploaded_file_path)
            # 更新 session 中的信息
            print('之前的' + request.session['info']['admin_image'])
            request.session['info'] = {'id': row_object.admin_id, 'name': row_object.name,
                                       'email': row_object.email,
                                       'admin_image': uploaded_file_path}
            print('之后的' + request.session['info']['admin_image'])
            # 把form中instance内容情况一下，防止render的时候会有多余的信息显示
            form = AdminAvatarModelForm()
            return render(request, 'admin_info.html', {'form': form})


def admin_logout(request):
    request.session.clear()
    return redirect('/login/')


def admin_update(request):
    if request.method == 'GET':
        form = AdminPasswordModelForm()
        return render(request, 'admin_pwd_update.html', {'form': form})
    else:
        admin_id = request.session['info']['id']
        row_object = Admin.objects.filter(admin_id=admin_id).first()
        original_password = row_object.password
        print(original_password)
        form = AdminPasswordModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            print(form.cleaned_data)
            information = form.cleaned_data
            # 验证原始密码
            print(information['original_password'] != str(original_password))
            if information['original_password'] != str(original_password):
                form.add_error('original_password', '原密码不正确')
                return render(request, 'admin_pwd_update.html', {'form': form})
            # 判断两次输入的密码是否相同
            password = information['password']
            confirm_password = information['confirm_password']
            if password == confirm_password:
                # 相同则保存到数据库中去
                form.save()
                return redirect('/login/')
            else:
                form.add_error('password', '两次输入的密码不一致')
                return render(request, 'admin_pwd_update.html',
                              {'form': form})
            pass

        else:
            return render(request, 'admin_pwd_update.html', {'form': form})
