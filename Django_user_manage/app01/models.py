from django.db import models

# Create your models here.
class Department(models.Model):
    """department table"""
    department = models.CharField(verbose_name='Department', max_length=32)

    def __str__(self):
        return self.department

class UserInfo(models.Model):
    """employee info"""
    name = models.CharField(verbose_name='Name', max_length=16)
    password = models.CharField(verbose_name='Password', max_length=64)
    age = models.IntegerField(verbose_name='Age')
    salary = models.DecimalField(verbose_name='Salary', max_digits=10,\
                                 decimal_places=2, default=2000)
    create_time = models.DateField(verbose_name='EntryDate')
    """
    Join Department
    On id
    """
    # this column will be named as depart_id
    # only id in Department table can appear in this col
    # if delete rows in Department table, also drop related records in this table
    # "on_delete=models.CASCADE"
    depart = models.ForeignKey(verbose_name='Department', to='Department', to_field='id', on_delete=models.CASCADE)
    # if delete rows in Department table, set related records NA in this table
    # "null=True, blank=True, on_delete=models.SET_NULL"
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    """
    also, if we do not want to connect to other tables, and the values are really simple,
    like "gender", only male and female,
    we can also use tuple
    """
    gender_choices = (
        (1, 'male'),
        (2, 'female')
    )
    gender = models.SmallIntegerField(verbose_name='gender', choices=gender_choices)



class Admin(models.Model):
    username = models.CharField(verbose_name='Admin_name', max_length=32)
    password = models.CharField(verbose_name='Password', max_length=64)

    def __str__(self):
        return self.username


class Task(models.Model):
    title = models.CharField(verbose_name="TaskTitle", max_length=64)
    detail = models.TextField(verbose_name="Detail")
    level_choices = {
        (1, 'serious'),
        (2, 'important'),
        (3, 'temporary'),
    }
    level = models.SmallIntegerField(verbose_name='Level', choices=level_choices, default=1)
    user = models.ForeignKey(verbose_name='Principal', to="Admin", on_delete=models.CASCADE)

class Order(models.Model):
    oid = models.CharField(verbose_name="Order ID", max_length=64)
    title = models.CharField(verbose_name="Name", max_length=64)
    price = models.IntegerField(verbose_name='Price')
    status_choice = {
        (1, "paid"),
        (2, "unpaid"),
    }
    status = models.SmallIntegerField(verbose_name="Status", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name='Administrator', to="Admin", on_delete=models.CASCADE)


class Profile(models.Model):
    name = models.CharField(verbose_name='Name', max_length=32)
    email = models.CharField(verbose_name='Email', max_length=64)
    img = models.CharField(verbose_name='Profile', max_length=128)

class City(models.Model):
    name = models.CharField(verbose_name='City', max_length=32)
    count = models.IntegerField(verbose_name='Population')
    img = models.FileField(verbose_name='LOGO', max_length=128, upload_to='city/')

