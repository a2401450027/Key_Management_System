# Generated by Django 5.0 on 2023-12-21 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyapp', '0008_alter_keys_kvector'),
    ]

    operations = [
        migrations.CreateModel(
            name='applys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sendid', models.IntegerField(verbose_name='sendID')),
                ('reserveid', models.IntegerField(verbose_name='reserveID')),
                ('sendname', models.CharField(default='小江', max_length=64, verbose_name='申请者姓名')),
                ('reservename', models.CharField(default='小江', max_length=64, verbose_name='审核者姓名')),
                ('level', models.IntegerField(default=0, verbose_name='申请等级')),
                ('status', models.CharField(default='待审核', max_length=64, verbose_name='申请状态')),
            ],
        ),
    ]
