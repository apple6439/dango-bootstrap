from django.db import models
from django.utils import timezone

# Create your models here.
# python manage.py makemigrations
# python manage.py migrate


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True, verbose_name='管理员ID')  # 管理员ID
    name = models.CharField(max_length=100, verbose_name='姓名')  # 姓名
    password = models.CharField(max_length=128, verbose_name='密码')  # 密码，建议使用哈希存储

    def __str__(self):
        return self.name  # 返回管理员姓名


class Department(models.Model):
    department_id = models.AutoField(primary_key=True, verbose_name='部门ID')  # 部门ID
    name = models.CharField(max_length=100, verbose_name='部门名称')  # 部门名称
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True,
                                related_name='managed_departments', verbose_name='部门负责人')  # 部门负责人
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='sub_departments', verbose_name='上级部门')  # 上级部门
    # auto_now_add为True时是不可编辑，反之。不可编辑意味着增删改查都无法改变
    created_at = models.DateTimeField(auto_now_add=False, verbose_name='创建时间')  # 创建时间
    performance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='部门业绩')  # 部门业绩

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [
        ('0', '男性'),
        ('1', '女性'),
    ]

    employee_id = models.AutoField(primary_key=True, verbose_name='员工ID')  # 员工ID
    name = models.CharField(max_length=100, verbose_name='姓名')  # 姓名
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')  # 性别
    hire_date = models.DateField(verbose_name='入职时间')  # 入职时间
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='薪资')  # 薪资
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees',
                                   verbose_name='所属部门')  # 所属部门

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, verbose_name='订单ID')  # 订单ID
    # 将产品图片存放在MEDIA_ROOT/product_images下
    product_image = models.ImageField(upload_to='product_images/', verbose_name='商品图片')  # 产品图片
    product_name = models.CharField(max_length=100, verbose_name='商品名称')  # 商品名称
    # auto_now_add为True时是不可编辑，反之。不可编辑意味着增删改查都无法改变
    order_date = models.DateTimeField(auto_now_add=False, verbose_name='订单时间',default=timezone.now)  # 订单时间
    quantity = models.PositiveIntegerField(verbose_name='订单数量')  # 订单数量，正整数
    customer_name = models.CharField(max_length=100, verbose_name='客户名称')  # 客户名称

    def __str__(self):
        return self.product_name  # 只返回商品名称
