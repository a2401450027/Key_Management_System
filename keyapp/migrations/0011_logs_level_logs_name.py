# Generated by Django 5.0 on 2023-12-24 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyapp', '0010_alter_userinfo_father'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='level',
            field=models.IntegerField(default=0, verbose_name='等级'),
        ),
        migrations.AddField(
            model_name='logs',
            name='name',
            field=models.CharField(default='小江', max_length=64, verbose_name='拥有者姓名'),
        ),
    ]