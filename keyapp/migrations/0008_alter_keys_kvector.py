# Generated by Django 5.0 on 2023-12-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyapp', '0007_keys_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='kvector',
            field=models.CharField(default='', max_length=8192, verbose_name='初始向量'),
        ),
    ]
