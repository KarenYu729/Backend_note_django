from django.shortcuts import render, redirect
from app01 import models
from django import forms

# Create your views here.
def depart_list(request):
    # get data from dataset
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})

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
    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.salary, obj.age)
    #     print(obj.create_time, obj.create_time.strftime('%Y-%m-%d'))
    #     print(obj.gender, obj.get_gender_display())
    #     print(obj.depart_id, obj.depart.department)

    return render(request, 'user_list.html', {'queryset': queryset})

class UserModelForm(forms.ModelForm):
    password = forms.CharField(min_length=8, label='password')
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'salary', 'create_time', 'gender', 'depart']
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        #     "salary": forms.TextInput(attrs={"class": "form-control"}),
        #     "create_time": forms.TextInput(attrs={"class": "form-control"}),
        #     "gender": forms.TextInput(attrs={"class": "form-control"}),
        #     "depart": forms.TextInput(attrs={"class": "form-control"})
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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


