"""
URL configuration for key_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from keyapp import views

urlpatterns = [
    # path('get_userinfo/', views.get_userinfo),
    path('main/', views.main),                  #主页
    path('keycreate/',views.key_create),        #密钥生成页面
    path('keysave/', views.keysave),            #保存生成的密钥
    path('keymanage/', views.keymanage),        #秘钥管理页面
    path('keydelete/', views.keydelete),        #删除密钥
    path('keychange/', views.keychange),        #修改密钥信息 只能改level和remark
    path('keysearch/', views.search),           #搜索密钥
    path('keylevel/', views.keylevel),          #分级管理页面
    path('applyit/', views.applyit),            #向上级申请对应等级权限
    path('agreeit/', views.agreeit),            #同意申请
    path('rejectit/', views.rejectit),          #拒绝申请
    path('applysearch/', views.applysearch),    #搜索向谁申请
    path('sonsearch/', views.sonsearch),        #搜索下级以及申请信息
    path('applydelete/', views.applydelete),    #删除申请信息
    path('sondelete/', views.sondelete),        #删除下级
    path('sonchange/', views.sonchange),        #修改下级权限
    path('logging/', views.logging),            #日志记录
    path('login/', views.login),                #登录
    path('logout/', views.logout),              #登出
    path('register/', views.register)           #注册
]
