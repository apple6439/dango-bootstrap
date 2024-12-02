"""
URL configuration for 后台管理系统 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from app01 import views

urlpatterns = [
    re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('admin/', admin.site.urls),
    # 登录页面
    path('login/', views.login),
    path('register/', views.register),
    # 系统首页
    path('home/', views.home),
    path('chart_data/', views.chart_data),
    # 员工
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/update/', views.user_update),
    path('user/<int:nid>/delete/', views.user_delete),  # 删除(多行和单行)
    # 部门
    path('department/list/', views.department_list),
    path('department/add/', views.department_add),
    path('department/<int:nid>/delete/', views.department_delete),  # 删除(多行和单行)
    path('department/<int:nid>/update/', views.department_update),
    # 订单
    path('order/list/', views.order_list),
    path('order/add/', views.order_add),
    path('order/<int:nid>/delete/', views.order_delete),  # 删除(多行和单行)
    path('order/<int:nid>/update/', views.order_update),  # 删除(多行和单行)
    # 管理员
    path('admin/info/', views.admin_info),
    path('admin/update/', views.admin_update),
    path('admin/logout/', views.admin_logout),
]
