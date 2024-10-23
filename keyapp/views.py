import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from keyapp.keycode import rsakey, deskey, aeskey, selfkey, sm4
from django import forms
from keyapp import models
from django.core.exceptions import ValidationError
from django.db.models import Q
import requests

# Create your views here.

# def get_userinfo(request):
#     data= requests.get('http://127.0.0.1:8000/get_userinfo/')
#     print(data,'jjjjj')
#     if data['session_data']:
#         user_id = data['session_data']['id']
#         username = data['session_data']['name']
#         request.session["info"] = {'id': user_id, 'name': username, 'flag': 'F'}
#         request.session['flag'] = {'flag': 'F'}
#         # 登录信息保存1小时
#         request.session.set_expiry(60 * 60 * 1)
#
#         return redirect("/main/")
#     else:
#         return redirect("/login/")


# 用户未登录


def main(request):
    if request.method == 'GET':
        name = request.session['info'].get('name')
        return render(request, 'main.html', {'name': name})
    try:
        print(request.session['info'].get('flag'))
    except:
        return JsonResponse({'status': False, 'error': '点击右上角头像登录'})


def null(request):
    return render(request, 'null.html')

# 生成密钥
def key_create(request):
    if request.method == "GET":
        name = request.session['info'].get('name')
        return render(request, 'key_creat.html', {'name': name})

    func = request.POST.get('func')
    level = request.POST.get('level')
    length = request.POST.get('length')
    if func == 'RSA':
        pkey, skey = rsakey.rsakey(int(length))
    elif func == 'DES':
        pkey, skey = deskey.deskey(int(length))
    elif func == 'AES':
        pkey, skey = aeskey.aeskey(int(length))
    else:
        pkey = selfkey.selfkey(int(length))
        skey = ''
    dt = datetime.datetime.now()
    models.Logs.objects.create(
        userID=request.session['info'].get('id'),
        name=request.session['info'].get('name'),
        father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
        thing='生成了一个' + func + '密钥, 长度为：' + str(length),
        date=dt.date(),
        time=dt.time().strftime("%H:%M:%S"),
    )
    result = {
        'pkey': pkey,
        'skey': skey,
        'func': func,
        'status': True
    }
    return JsonResponse({'pkey': pkey, 'skey': skey, 'func': func, 'status': True})


# 保存密钥
def keysave(request):
    func = request.POST.get('func')
    level = request.POST.get('level')
    length = request.POST.get('length')
    pkey = request.POST.get('pkey')
    skey = request.POST.get('skey')
    remark = request.POST.get('remark')
    id = request.session['info'].get('id')
    print(pkey, skey, '33333')
    pkey = sm4.SM4(pkey, 'hdfuivndufvhnodui099', '1')
    skey = sm4.SM4(skey, 'hdfuivndufvhnodui099', '1')
    models.Keys.objects.create(
        userID=id,
        username=request.session['info'].get('name'),
        key=pkey,
        kvector=skey,
        method=func,
        level=level,
        length=length,
        remark=remark
    )
    dt = datetime.datetime.now()
    models.Logs.objects.create(
        userID=request.session['info'].get('id'),
        name=request.session['info'].get('name'),
        father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
        thing='保存了一个' + func + '密钥, 长度为：' + str(length),
        date=dt.date(),
        time=dt.time().strftime("%H:%M:%S"),
    )
    return JsonResponse({'status': True})


# 管理密钥
def keymanage(request):
    if request.method == 'GET':
        me = models.UserInfo.objects.filter(id=request.session['info'].get('id')).first()
        form = models.Keys.objects.filter(
            Q(userID=request.session['info'].get('id')) | (Q(userID=me.father) & Q(level__lte=me.level)))
        for item in form:
            item.key = sm4.SM4(item.key, 'hdfuivndufvhnodui099', '0')
            item.kvector = sm4.SM4(item.kvector, 'hdfuivndufvhnodui099', '0')
        search = request.GET.get('search')
        if me.father != 0:
            fname = models.UserInfo.objects.filter(id=me.father).first().name
        else:
            fname = '无'
        name = request.session['info'].get('name')
        return render(request, 'keymanage.html', {'form': form, 'fname': fname, 'flevel': me.level, 'name': name})
    search = request.GET.get('search')
    print(search, '2')
    return render(request, 'keymanage.html')


# 删除密钥:
def keydelete(request):
    print('1111')
    try:
        pid = request.POST.get('id')
        form = models.Keys.objects.filter(id=pid).first()
        models.Keys.objects.filter(id=pid).delete()
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='删除id为' + str(pid) + '的密钥，密钥拥有者：' + str(form.usename),
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 密钥信息检索
def search(request):
    info = request.GET.get('search')
    print(info, '9999')
    try:
        lev = int(info)
        form = models.Keys.objects.filter(
            Q(userID=request.session['info'].get('id')) & (Q(remark__contains=info) | Q(level=lev)))
    except:
        form = models.Keys.objects.filter(Q(userID=request.session['info'].get('id')) & Q(remark__contains=info))
    return render(request, 'keymanage.html', {'form': form})


# 修改密钥信息
def keychange(request):
    try:
        pid = request.POST.get('id')
        level = int(str(request.POST.get('level')).split('：')[1])
        form = models.Keys.objects.filter(id=pid).first()
        me = models.UserInfo.objects.filter(id=request.session['info'].get('id')).first()
        if level > me.level and form.userID != request.session['info'].get('id'):
            return JsonResponse({'status': False, 'err': '权限不足'})
        remark = str(request.POST.get('remark')).split('：')[1]
        print(pid, level, remark, '898')
        models.Keys.objects.filter(id=pid).update(
            level=level,
            remark=remark
        )
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='修改id为' + str(pid) + '的密钥等级为' + str(level) + '级，' + '备注为' + str(remark),
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False, 'err': '联系管理员出错了'})


# 分级管理
def keylevel(request):
    if request.method == 'GET':
        pid = request.session['info'].get('id')
        makeform = models.applys.objects.filter(reserveid=pid)
        form1 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=1))
        form2 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=2))
        form3 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=3))
        name = request.session['info'].get('name')
        me = models.UserInfo.objects.filter(id=request.session['info'].get('id')).first()
        if me.father != 0:
            fname = models.UserInfo.objects.filter(id=me.father).first().name
        else:
            fname = '无'
        return render(request, 'keylevel.html',
                      {"makeform": makeform, "form1": form1, "form2": form2, "form3": form3, 'name': name,
                       'fname': fname, 'flevel': me.level})


# 申请权限
def applyit(request):
    try:
        rid = request.POST.get('id')
        rname = models.UserInfo.objects.filter(id=rid).first().name
        sid = request.session['info'].get('id')
        sname = request.session['info'].get('name')
        level = request.POST.get('level')
        models.applys.objects.create(
            sendid=sid,
            sendname=sname,
            reserveid=rid,
            reservename=rname,
            level=level,
        )
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing=str(sname) + '提出向' + str(rname) + '申请' + str(
                level) + '级权限的申请信息',
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 搜索申请权限
def applysearch(request):
    info = request.GET.get('search')
    print(info, '9999')
    form = models.UserInfo.objects.filter(user=info)
    pid = request.session['info'].get('id')
    makeform = models.applys.objects.filter(reserveid=pid)
    form1 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=1))
    form2 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=2))
    form3 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=3))

    return render(request, 'keylevel.html',
                  {"makeform": makeform, "form1": form1, "form2": form2, "form3": form3, 'applyform': form,
                   'flag': 'A'})


# 搜索拥有当前用户权限的下级
def sonsearch(request):
    info = request.GET.get('search')
    print(info, '9999')
    pid = request.session['info'].get('id')
    try:
        sid = int(info)
        makeform = models.applys.objects.filter(Q(level=sid) & Q(reserveid=pid))
        form1 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=1) & Q(level=sid))
        form2 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=2) & Q(level=sid))
        form3 = models.UserInfo.objects.filter(Q(father=pid) & Q(level=3) & Q(level=sid))
    except:
        makeform = models.applys.objects.filter(Q(sendname__contains=info) & Q(reserveid=pid))
        form1 = models.UserInfo.objects.filter(
            (Q(user__contains=info) | Q(name__contains=info)) & Q(level=1) & Q(father=pid))
        form2 = models.UserInfo.objects.filter(
            Q(father=pid) & Q(level=2) & (Q(user__contains=info) | Q(name__contains=info)))
        form3 = models.UserInfo.objects.filter(
            Q(father=pid) & Q(level=3) & (Q(user__contains=info) | Q(name__contains=info)))

    return render(request, 'keylevel.html',
                  {"makeform": makeform, "form1": form1, "form2": form2, "form3": form3, 'flag': 'S'})


# 同意申请
def agreeit(request):
    pid = request.POST.get('id')
    print(pid)
    try:
        pid = request.POST.get('id')
        form = models.applys.objects.filter(id=pid).first()
        models.applys.objects.filter(id=pid).update(
            status='已同意'
        )
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='同意' + str(form.sendname) + '向' + str(form.reservename) + '申请' + str(
                form.level) + '级权限的申请信息',
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        form = models.applys.objects.filter(id=pid).first()
        models.UserInfo.objects.filter(id=form.sendid).update(
            father=request.session['info'].get('id'),
            level=form.level
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 拒绝申请
def rejectit(request):
    try:
        pid = request.POST.get('id')
        form = models.applys.objects.filter(id=pid).first()
        models.applys.objects.filter(id=pid).update(
            status='已拒绝'
        )
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='拒绝' + str(form.sendname) + '向' + str(form.reservename) + '申请' + str(
                form.level) + '级权限的申请信息',
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 删除申请信息
def applydelete(request):
    print('applydelete')
    try:
        pid = request.POST.get('id')
        form = models.applys.objects.filter(id=pid).first()
        models.applys.objects.filter(id=pid).delete()
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='删除' + str(form.sendname) + '向' + str(form.reservename) + '申请' + str(
                form.level) + '级权限的申请信息',
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 删除下级
def sondelete(request):
    print('sondelete')
    try:
        pid = request.POST.get('id')
        form = models.UserInfo.objects.filter(id=pid).first()
        models.UserInfo.objects.filter(id=pid).update(
            father=0,
            level=0
        )
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='删除' + str(form.name) + '的上级信息：来自' + str(
                models.UserInfo.objects.filter(id=form.father).first().name) + '的' + str(
                form.level) + '级权限',
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 修改下级权限
def sonchange(request):
    try:
        pid = request.POST.get('id')
        level = int(str(request.POST.get('level')).split('：')[1])
        print(pid, level, '898')
        form = models.UserInfo.objects.filter(id=pid).first()
        models.UserInfo.objects.filter(id=pid).update(
            level=level
        )
        dt = datetime.datetime.now()
        models.Logs.objects.create(
            userID=request.session['info'].get('id'),
            name=request.session['info'].get('name'),
            father=models.UserInfo.objects.filter(id=request.session['info'].get('id')).first().father,
            thing='修改' + str(form.name) + '来自上级' + str(
                models.UserInfo.objects.filter(id=form.father).first().name) + '权限为' + str(
                level) + '级',
            date=dt.date(),
            time=dt.time().strftime("%H:%M:%S"),
        )
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


# 日志记录
def logging(request):
    if request.method == 'GET':
        form = models.Logs.objects.filter(
            Q(userID=request.session['info'].get('id')) | Q(father=request.session['info'].get('id')))
        return render(request, 'logging.html', {'form': form})


class LoginUserForm(forms.Form):
    user = forms.CharField(label="账号", widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(render_value=True, attrs={"class": "form-control"}),
                               required=True)
    key = forms.CharField(label="key", widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if pwd == None:
            raise ValidationError('请输入密码')
        return (pwd)

    def clean_user(self):
        user = self.cleaned_data['user']
        if not user:
            raise ValidationError('请输入账号')
        return user


def login(request):
    if request.method == "GET":
        form = LoginUserForm()
        return render(request, 'login.html', {"form": form})
    form = LoginUserForm(data=request.POST)
    if form.is_valid():
        user = form.clean_user()
        password = form.clean_password()
        # master_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        master_object = models.UserInfo.objects.filter(user=user).first()
        if not master_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})
        # cookie

        request.session["info"] = {'id': master_object.id, 'name': master_object.name, 'user': master_object.user,
                                   'flag': 'F'}
        request.session['flag'] = {'flag': 'F'}
        # 登录信息保存1小时
        request.session.set_expiry(60 * 60 * 1)

        return redirect("/main/")

    return render(request, 'login.html', {"form": form})


class RegisterForm(forms.Form):
    user = forms.CharField(label="账号", widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    name = forms.CharField(label="姓名", widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(render_value=True, attrs={"class": "form-control"}),
                               required=True)
    con_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.UserInfo
        fields = ['user', 'name', 'password', 'con_password']

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if len(pwd) < 8:
            raise ValidationError('密码长度不能小于8')
        return (pwd)

    def clean_user(self):
        user = self.cleaned_data['user']
        if models.UserInfo.objects.filter(user=user).exists():
            raise ValidationError('账号已存在')
        return user

    def clean_name(self):
        name = self.cleaned_data['name']
        # if models.UserInfo.objects.filter(user=user).exists():
        #     raise ValidationError('账号已存在')
        return name

    def clean_con_password(self):
        pwd = self.cleaned_data.get("password")
        con = (self.cleaned_data.get("con_password"))
        if pwd != con:
            raise ValidationError("密码不一致，请重新输入")
        return con


# 注册
def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterForm(data=request.POST)
    print(form)
    if form.is_valid():
        user = form.clean_user()
        name = form.clean_name()
        password = form.clean_password()
        models.UserInfo.objects.create(
            user=request.POST.get('user'),
            name=request.POST.get('name'),
            password=request.POST.get('password'),
            level='0',
            key='0',
        )
        print('11111111111111111111111111111111111111111111')
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def logout(request):
    request.session.clear()
    return redirect('/main/')
