from django.db import models


# Create your models here.
# python manage.py makemigrations
# python manage.py migrate


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)  # 管理员ID
    name = models.CharField(max_length=100)  # 姓名
    password = models.CharField(max_length=128)  # 密码，建议使用哈希存储

    def __str__(self):
        return self.name  # 返回管理员姓名


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)  # 部门ID
    name = models.CharField(max_length=100)  # 部门名称
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True,
                                related_name='managed_departments')  # 部门负责人
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='sub_departments')  # 上级部门
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    performance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 部门业绩

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
    ]

    employee_id = models.AutoField(primary_key=True)  # 员工ID
    name = models.CharField(max_length=100)  # 姓名
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # 性别
    hire_date = models.DateField()  # 入职时间
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # 薪资
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')  # 所属部门

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  # 订单ID
    product_image = models.ImageField(upload_to='product_images/')  # 产品图片
    product_name = models.CharField(max_length=100)  # 商品名称
    quantity = models.PositiveIntegerField()  # 订单数量
    customer_name = models.CharField(max_length=100)  # 客户名称

    def __str__(self):
        return self.product_name  # 只返回商品名称
