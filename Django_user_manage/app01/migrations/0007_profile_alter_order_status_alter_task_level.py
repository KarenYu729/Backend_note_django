# Generated by Django 4.2.1 on 2023-05-17 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_alter_task_level_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('email', models.CharField(max_length=64, verbose_name='Email')),
                ('img', models.CharField(max_length=128, verbose_name='Profile')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(2, 'unpaid'), (1, 'paid')], default=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='level',
            field=models.SmallIntegerField(choices=[(3, 'temporary'), (1, 'serious'), (2, 'important')], default=1, verbose_name='Level'),
        ),
    ]