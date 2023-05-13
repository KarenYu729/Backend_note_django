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
    create_time = models.DateTimeField(verbose_name='EntryDate')
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