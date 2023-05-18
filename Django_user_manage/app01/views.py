from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from django.utils.safestring import mark_safe
import math
from app01.utils.pageination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5

# error message
from django.core.exceptions import ValidationError

from app01.utils.code import check_code
from io import BytesIO

from django.http import JsonResponse


# Create your views here.
def depart_list(request):
    # # get data from dataset
    # queryset = models.Department.objects.all()
    #
    # return render(request, 'depart_list.html', {'queryset': queryset})
    queryset = models.Department.objects.all().order_by('-id')
    page_object = Pagination(request, queryset, page_size=4)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        'queryset': page_queryset,
        'page_string': page_string
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    depart_title = request.POST.get('Depart')
    models.Department.objects.create(department=depart_title)
    return redirect('/depart/list/')


def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()

    return redirect('/depart/list/')


def depart_edit(request, nid):
    if request.method == 'GET':
        row_obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_obj": row_obj})

    depart = request.POST.get('Depart')
    models.Department.objects.filter(id=nid).update(department=depart)
    return redirect('/depart/list/')


def user_list(request):
    """
    # get total number of record
    total_count = models.UserInfo.objects.all().count()

    # page, default value=1
    page = int(request.GET.get('page', 1))
    page_size = 5
    start = (page-1)*page_size
    end = page*page_size

    # total pages
    total_page = math.ceil(total_count / page_size)

    plus = 2
    if total_page <= 2 * plus + 1:
        start_page = 1
        end_page = total_page
    else:
        if page <= plus:
            start_page = 1
            end_page = 2 * plus +1
        elif page <= total_page - plus:
            start_page = page - plus
            end_page = page + plus
        else:
            start_page = total_page - 2*plus
            end_page = total_page

    queryset = models.UserInfo.objects.all()[start:end]
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.salary, obj.age)
    #     print(obj.create_time, obj.create_time.strftime('%Y-%m-%d'))
    #     print(obj.gender, obj.get_gender_display())
    #     print(obj.depart_id, obj.depart.department)

    page_str_list = []
    # add first page
    front = '<li><a href="/user/list/?page={}">Front page</a></li>'.format(1)
    page_str_list.append(front)
    # add previous page
    if page > 1:
        prev = '<li><a href="/user/list/?page={}">&laquo;</a></li>'.format(page-1)
    else:
        prev = '<li><a href="/user/list/?page={}">&laquo;</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page+1):
        if i == page:
            ele = '<li class="active"><a href="/user/list/?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="/user/list/?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)

    # add next page
    if page < total_page:
        prev = '<li><a href="/user/list/?page={}">&raquo;</a></li>'.format(page+1)
    else:
        prev = '<li><a href="/user/list/?page={}">&raquo;</a></li>'.format(total_page)
    page_str_list.append(prev)

    # add last page
    last = '<li><a href="/user/list/?page={}">Front page</a></li>'.format(total_page)
    page_str_list.append(last)

    page_string = mark_safe("".join(page_str_list))

    return render(request, 'user_list.html', {'queryset': queryset, 'page_string': page_string})
    """
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict['name__contains'] = search_data
    queryset = models.UserInfo.objects.filter(**data_dict).order_by('-age')
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        'queryset': page_queryset,
        'page_string': page_string,
        'search_data': search_data
    }

    return render(request, 'user_list.html', context)


# class UserModelForm(forms.ModelForm):
#     password = forms.CharField(min_length=8, label='password')
#     class Meta:
#         model = models.UserInfo
#         fields = ['name', 'password', 'age', 'salary', 'create_time', 'gender', 'depart']
#         # widgets = {
#         #     "name": forms.TextInput(attrs={"class": "form-control"}),
#         #     "password": forms.TextInput(attrs={"class": "form-control"}),
#         #     "age": forms.TextInput(attrs={"class": "form-control"}),
#         #     "salary": forms.TextInput(attrs={"class": "form-control"}),
#         #     "create_time": forms.TextInput(attrs={"class": "form-control"}),
#         #     "gender": forms.TextInput(attrs={"class": "form-control"}),
#         #     "depart": forms.TextInput(attrs={"class": "form-control"})
#         # }
#         # widgets = {"create_time": forms.TextInput(attrs={"type": "date"})}
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for name, field in self.fields.items():
#             field.widget.attrs = {"class": "form-control", "placeholder": field.label}
class UserModelForm(BootStrapModelForm):
    password = forms.CharField(min_length=8, label='password')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'salary', 'create_time', 'gender', 'depart']


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()

        return render(request, 'user_add.html', {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    # error message
    return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    # get data from database used nid
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    # get data from POST, save data to id=nid
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.save: save all info from custom input in form
        # if we have some info which does not from custom input
        # we have:
        # from.instance.<keyName> = <value>
        form.save()
        return redirect('/user/list/')
    # error message
    return render(request, 'user_add.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def admin_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict['name__contains'] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data
    }

    return render(request, 'admin_list.html', context)


class AdminModelForm(BootStrapModelForm):
    # confirm_password = forms.CharField(label='Password_conform',
    #                                    widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(label='Password_conform',
                                       widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            # 'password': forms.PasswordInput(render_value=True),
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        # we will exe clean password, return encrypt password
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        # what we get are already been encrypted,
        # thus we also need to encrypted password confirm for later confirm
        confirm = md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("Password not match")
        return confirm


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        context = {
            'title': 'Add Administrator',
            'form': form,
        }

        return render(request, 'change.html', context)

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # get all input
        # form.cleaned_data

        form.save()

        return redirect('/admin/list/')

    context = {
        'title': 'Add Administrator',
        'form': form,
    }
    return render(request, 'change.html', context)


class AdminEditModelForm(BootStrapModelForm):
    # confirm_password = forms.CharField(label='Password_conform',
    #                                    widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(label='Password_conform',
                                       widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            # 'password': forms.PasswordInput(render_value=True),
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        # we will exe clean password, return encrypt password
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # self.instance: object we pass through instance
        # AdminEditModelForm(instance=row_object)
        # thus self.instance -> row_object
        # self.instance.pk (primary key-> id)
        exist = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).first()
        if exist:
            raise ValidationError("Can not use previous password")

        return md5(pwd)

    def clean_confirm_password(self):
        # what we get are already been encrypted,
        # thus we also need to encrypted password confirm for later confirm
        confirm = md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("Password not match")
        return confirm


def admin_edit(request, nid):
    # check if id exist
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        context = {
            'title': 'Edit Administrator',
            'form': form,
        }
        return render(request, 'change.html', context)

    form = AdminEditModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        # form.save()
        return redirect('/admin/list/')

    context = {
        'title': 'Edit Administrator',
        'form': form,
    }
    return render(request, 'change.html', context)


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput,
                               required=True)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput,
                               required=True)
    code = forms.CharField(label="verify",
                           widget=forms.TextInput,
                           required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {"class": "form-control",
                                      "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


# allow access if login
# ! Disable access for users haven't logged in
# ->admin_list/user_list/depart_list
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)

    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Verification Code incorrect")
            return render(request, 'login.html', {'form': form})

        # form.cleaned_data (type:dict)
        # find record in dict where username, password = username, password
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error("password", "Username or Password incorrect")
            return render(request, 'login.html', {'form': form})

        # add cookie & session
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # reset expiry time
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list/")
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    img, code_string = check_code()

    request.session['image_code'] = code_string
    # set verification code only valid in 1 min
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    stream.getvalue()
    return HttpResponse(stream.getvalue())


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea
            "detail": forms.TextInput,
        }


def task_list(request):
    queryset = models.Task.objects.all().order_by('id')

    form = TaskModelForm()
    page_object = Pagination(request, queryset, page_size=2)

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'task_list.html', context)


# # GET
# def task_ajax(request):
#     return HttpResponse('success!^-^')


# POST
from django.views.decorators.csrf import csrf_exempt
import json


# from django.http import JsonResponse
@csrf_exempt
def task_ajax(request):
    print(request.POST)

    data_dict = {"status": True, "data": [11, 22, 33, 44]}

    return HttpResponse(json.dumps(data_dict))
    # return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    print(request.POST)
    # method 1
    # Use ModelForm

    form = TaskModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}

    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ['oid', 'admin']


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')

    form = OrderModelForm()
    page_object = Pagination(request, queryset, page_size=5)

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'order_list.html', context)


import random
from datetime import datetime


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # add oid
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # get current account id
        form.instance.admin_id = request.session['info']['id']

        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def order_delete(request):
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"statues": False, 'error': 'No such order'})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    uid = request.GET.get('uid')
    row_dict = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not row_dict:
        JsonResponse({'status': False, 'error': 'No such order'})

    return JsonResponse({"status": True, 'data': row_dict})


@csrf_exempt
def order_edit(request):
    uid = request.GET.get('uid')
    row_object = models.Order.object.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"statues": False, 'tips': 'No such order'})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    JsonResponse({'status': False, 'error': form.errors})


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    legend = ['sales', 'predictions']
    x_axis = ['shirt', 'cardigan', 'chiffon', 'pants', 'heels', 'socks']

    series_list = [
        {
            "name": 'sales',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": 'predictions',
            "type": 'bar',
            "data": [10, 18, 45, 2, 5, 30]
        }
    ]
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    series_list = [
        {"value": 1048, "name": 'Search Engine'},
        {"value": 735, "name": 'Direct'},
        {"value": 580, "name": 'Email'},
        {"value": 484, "name": 'Union Ads'},
        {"value": 300, "name": 'Video Ads'}
    ]
    result = {
        "status": True,
        "data": {
            "series_list": series_list,
        }
    }
    return JsonResponse(result)

def chart_line(request):
    series_list = [
                    {
                        "name": 'Email',
                        "type": 'line',
                        "stack": 'Total',
                        "data": [120, 132, 101, 134, 90, 230, 210]
                    },
                    {
                        "name": 'Union Ads',
                        "type": 'line',
                        "stack": 'Total',
                        "data": [220, 182, 191, 234, 290, 330, 310]
                    },
                    {
                        "name": 'Video Ads',
                        "type": 'line',
                        "stack": 'Total',
                        "data": [150, 232, 201, 154, 190, 330, 410]
                    },
                    {
                        "name": 'Direct',
                        "type": 'line',
                        "stack": 'Total',
                        "data": [320, 332, 301, 334, 390, 330, 320]
                    }
                ]
    result = {
        "status": True,
        "data": {
            "series_list": series_list,
        }
    }
    return JsonResponse(result)

import pandas as pd
def upload_list(request):
    file_object = request.FILES.get('exc')
    print(file_object)
    df = pd.read_csv(file_object)
    print(df['type'][2])
    for i in range(2, 4):
        text = df['type'][i]
        exist = models.Department.objects.filter(department=text).exists()
        if not exist:
            models.Department.objects.create(department=text)

    # return render(request, 'upload_list.html')
    # return HttpResponse("^-^")
    return redirect('/depart/list/')

class Upform(forms.Form):
    name = forms.CharField(label='Name')
    email = forms.CharField(label='Email')
    img = forms.FileField(label='Profile')
    exclude_files = ['img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in self.exclude_files:
                continue
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {"class": "form-control",
                                      "placeholder": field.label}
import os
from django.conf import settings
def upload_form(request):
    title = 'Profile'
    if request.method == "GET":
        form = Upform()
        context = {
            'form': form,
            'title': title
        }
        return render(request, 'upload_form.html', context)

    form = Upform(data=request.POST, files=request.FILES)
    if form.is_valid():
        # save img
        # save img direction to database
        image_object = form.cleaned_data.get('img')

        # # file path in Linux & windows are diff
        # db_file_path = os.path.join("static", "img", image_object.name)
        # file_path = os.path.join("app01", db_file_path)
        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join('media', image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        models.Profile.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            img=media_path,
        )

        return HttpResponse("^-^")
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'upload_form.html', context)

def med(request):
    return HttpResponse("-_-")

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


def upload_ModelFrom(request):
    title = 'City'
    if request.method == "GET":
        form = UpModelForm()
        context = {
            'form': form,
            'title': title
        }
        return render(request, 'upload_form.html', context)

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("^-^")
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'upload_form.html', context)
    # return HttpResponse("o_O")

def city_list(request):

    queryset = models.City.objects.all()

    return render(request, 'city_list.html', {'queryset': queryset})

