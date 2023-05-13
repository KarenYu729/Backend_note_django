# Generated by Django 4.2.1 on 2023-05-12 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=32, verbose_name='Department')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Name')),
                ('password', models.CharField(max_length=64, verbose_name='Password')),
                ('age', models.IntegerField(verbose_name='Age')),
                ('salary', models.DecimalField(decimal_places=2, default=2000, max_digits=10, verbose_name='Salary')),
                ('create_time', models.DateTimeField(verbose_name='EntryDate')),
                ('gender', models.SmallIntegerField(choices=[(1, 'male'), (2, 'female')], verbose_name='gender')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.department')),
            ],
        ),
    ]