# Generated by Django 5.0 on 2023-12-20 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyapp', '0002_keys_kvector_keys_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='keys',
            name='length',
            field=models.IntegerField(default=0, verbose_name='长度'),
        ),
    ]
