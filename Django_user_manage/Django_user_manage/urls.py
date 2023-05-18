"""
URL configuration for Django_user_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('med/', views.med),

    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),

    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/delete/', views.admin_delete),

    path('login/', views.login),
    path('logout/', views.logout),
    path('image/code/', views.image_code),

    path('task/list/', views.task_list),
    path('task/ajax/', views.task_ajax),
    path('task/add/', views.task_add),

    path('order/list/', views.order_list),
    path('order/add/', views.order_add),
    path('order/delete/', views.order_delete),
    path('order/detail/', views.order_detail),
    path('order/edit/', views.order_edit),

    path('chart/list/', views.chart_list),
    path('chart/bar/', views.chart_bar),
    path('chart/pie/', views.chart_pie),
    path('chart/line/', views.chart_line),

    path('upload/list/', views.upload_list),
    path('upload/form/', views.upload_form),
    path('upload/model/form/', views.upload_ModelFrom),
    path('city/list/', views.city_list),
]
