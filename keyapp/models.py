from django.db import models
import datetime
# Create your models here.
class UserInfo(models.Model):
    user = models.CharField(verbose_name="账号", max_length=32)
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    level = models.IntegerField(verbose_name="等级", default=0)
    key = models.CharField(verbose_name="key", max_length=64, default='')
    father = models.IntegerField(verbose_name="上级", max_length=32, default=0)

class Keys(models.Model):
    userID = models.IntegerField(verbose_name="userID")
    username = models.CharField(verbose_name="拥有者姓名",max_length=64,default='小江')
    key = models.CharField(verbose_name="密钥",max_length=9*1024)
    kvector = models.CharField(verbose_name="初始向量",max_length=8*1024, default='')
    method = models.CharField(verbose_name="密钥类型", max_length=64, default='')
    level = models.IntegerField(verbose_name="等级", default=0)
    length = models.IntegerField(verbose_name="长度", default=0)
    remark = models.CharField(verbose_name="备注",max_length=1024, default='')

class Logs(models.Model):
    userID = models.IntegerField(verbose_name="userID")
    name = models.CharField(verbose_name="拥有者姓名", max_length=64, default='小江')
    level = models.IntegerField(verbose_name="等级", default=0)
    father = models.IntegerField(verbose_name="上级", max_length=32, default=0)
    thing = models.CharField(verbose_name="动作", max_length=64, null=True, blank=True)
    time = models.TimeField(verbose_name="时间", default=datetime.time(0, 0))
    date = models.DateField(verbose_name="日期", default=datetime.date(2023, 1, 1))

class applys(models.Model):
    sendid = models.IntegerField(verbose_name="sendID")
    reserveid = models.IntegerField(verbose_name="reserveID")
    sendname = models.CharField(verbose_name="申请者姓名", max_length=64, default='小江')
    reservename = models.CharField(verbose_name="审核者姓名", max_length=64, default='小江')
    level = models.IntegerField(verbose_name="申请等级", default=0)
    status = models.CharField(verbose_name="申请状态", max_length=64, default='待审核')
#111