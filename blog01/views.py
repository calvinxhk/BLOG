from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from blog01 import models,forms
from statics.plugins.piccode import piccode
from io import BytesIO
import time


def index(request):
    '''
    主站页面
    :param request:
    :return:
    '''
    if request.method =='GET':
        uid = request.session.get('uid')
        data = models.User.objects.filter(uid=uid).first()
        return render(request,'blog/index.html',{'data':data})




def logconfirm(wrapper):
    '''
    登录状态装饰器
    :param wrapper:
    :return:
    '''
    def fun(request,*args,**kwargs):
        if request.session.get('uid'):
            res = wrapper(request,*args,**kwargs)
            return res
        else:
            return redirect('/login.html')
    return fun


def register(request):
    '''
        注册函数，通过form组件验证和生成html，iframe伪造ajax上传图片，随机验证码，完成注册页面业务

        :param request:
        :return:
        '''
    if request.method == 'GET':
        form = forms.Register(request)
        return render(request, 'blog/register.html', {'form': form, })
    else:
        form = forms.Register(request, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            data = models.User.objects.filter(name=name)
            if not data:
                form.cleaned_data.pop('pwd2')
                form.cleaned_data.pop('piccode')
                rg_time = time.time()
                form.cleaned_data['rg_time'] = rg_time
                import os
                img = request.FILES.get('avatar')
                file_path = os.path.join('static/images/avatar', str(time.time()) + img.name)
                with open(file_path, 'wb') as f:
                    for chun in img.chunks():
                        f.write(chun)
                form.cleaned_data['avatar'] = file_path
                models.User.objects.create(**form.cleaned_data)
                return redirect('/login.html')
            else:
                msg = '账号已存在'
                return render(request, 'blog/register.html', {'form': form, 'msg': msg})
        return render(request, 'blog/register.html', {'form': form})


def check_code(request):
    '''
    返回验证图片
    :param request:
    :return:
    '''
    img, code = piccode(120, 30)
    stream = BytesIO()
    img.save(stream, 'png')
    codedata = stream.getvalue()
    request.session['piccode'] =code
    return HttpResponse(codedata)


def login(request):
    '''
        登录函数
        :param request:
        :return:
        '''
    if request.method == 'GET':
        uid = request.session.get('uid')
        if uid:
            return redirect('/home/%s.html' % uid)
        form = forms.Login(request)
        return render(request, 'blog/login.html', {'form': form})
    else:
        form = forms.Login(request, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            session = request.POST.get('logrecord')
            data = models.User.objects.filter(name=name, pwd=pwd).first()
            if data:
                request.session['uid'] = data.uid
                if session:
                    request.session.set_expiry(259200)
                return redirect('/home/%s.html' % data.uid)
        form = forms.Login(request, request.POST)
        msg = '用户名或密码错误'
        return render(request, 'blog/login.html', {'form': form, 'msg': msg})


def logout(request):
    '''
    退出登录状态
    :param request:
    :return:
    '''
    del request.session['uid']
    return redirect('/login.html')


def retrieve(request):
    '''
    找回密码页面
    :param request:
    :return:
    '''
    if request.method =='GET':
        form = forms.Retrieve(request)
        return render(request,'blog/retrieve.html',{'form':form})
    else:
        form = forms.Retrieve(request,request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            data = models.User.objects.filter(name=name,email=email,phone=phone).first()
            if name and email and phone and data:
                return render(request,'blog/retrieve.html',{'form':form,'data':data})
        return render(request,'blog/retrieve.html',{'form':form})


def home(request,param):
    '''
    个人主页,展示个人详细信息
    :param request:
    :return:
    '''
    id = param
    data = models.User.objects.filter(uid=id).first()
    return render(request,'blog/home.html',{'data':data})


@logconfirm
def blog_register(request):
    '''
    博客注册
    :param request:
    :return:
    '''
    if request.method =='GET':
        uid = request.session.get('uid')
        data = models.User.objects.filter(uid=uid).first()
        if not data.blogname:
            form = forms.Blog(request)
            return render(request,'blog/blog_register.html',{"form":form})
        else:
            return HttpResponse('已经注册过了')
    else:
        form = forms.Blog(request,request.POST)
        if form.is_valid():
            blogname = form.cleaned_data.get('name')
            data = models.BlogInfo.objects.filter(blogname=blogname)
            if not data:
                import time
                rgtime = time.time()
                new = models.BlogInfo.objects.create(blogname=blogname,rgtime=rgtime)
                uid = request.session.get('uid')
                models.User.objects.filter(uid=uid).update(blogname=new)
                return redirect('/blog/{}/'.format(blogname))
            else:
                msg = '账号已被注册'
        return render(request,'blog/blog_register.html',{"form":form,"msg":msg})


def blog(request,param):
    '''

    :param request:
    :param param: 博客id
    :return:
    '''
    if request.method == 'GET':

        data = models.BlogInfo.objects.filter(blogname=param).first()

        if not data :
            return render(request,'blog/404.html')
        return render(request,'blog/blog.html',{'param':param})

@logconfirm
def posts(request):
    uid = request.session.get('uid')
    data = models.User.objects.filter(uid=uid).first()
    return render(request,'blog/posts.html',{'data':data})

@logconfirm
def editor(request):
    return render(request,'blog/blogedit.html')

urlpatterns=[
    url(r'^register\.html$',register),
    url(r'^check_code/',check_code),
    url(r'^login\.html$',login),
    url(r'^home/(\d+)\.html$',home),
    url(r'^logout\.html$',logout),
    url(r'^retrieve\.html$',retrieve),
    url(r'^blogregister\.html$',blog_register),
    url(r'^blog/(.*)/$',blog),
    url(r'^posts$',posts),
    url(r'^editor$',editor),
    url(r'', index)
]







