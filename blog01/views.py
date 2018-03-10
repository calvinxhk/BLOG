from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from io import BytesIO
from blog01 import models,forms
from static.plugins.piccode import piccode


def index(request):
    """
    主站页面
    :param request:
    :return:
    """
    if request.method =='GET':
        return render(request,'blog/index.html')


def register(request):
    """
        注册函数，通过form组件验证和生成html，iframe伪造ajax上传图片，随机验证码，完成注册页面业务

        :param request:
        :return:
     """
    if request.method == 'GET':
        form = forms.Register(request)
        return render(request, 'blog/register.html', {'form': form, })
    else:
        form = forms.Register(request, request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            data = models.UserInfo.objects.filter(username=username)
            if not data:
                form.cleaned_data.pop('password2')
                form.cleaned_data.pop('piccode')
                models.UserInfo.objects.create_user(**form.cleaned_data)
                return redirect('/login.html')
            else:
                msg = '账号已存在'
                return render(request, 'blog/register.html', {'form': form, 'msg': msg})
        return render(request, 'blog/register.html', {'form': form})


def check_code(request):
    """
    返回验证图片
    :param request:
    :return:
    """
    img, code = piccode(120, 30)
    stream = BytesIO()
    img.save(stream, 'png')
    codedata = stream.getvalue()
    request.session['piccode'] =code
    return HttpResponse(codedata)


def user_login(request):
    '''
        登录函数
        :param request:
        :return:
        '''
    if request.method == 'GET':
        if  request.user.is_authenticated():
            return redirect('/home/%s.html' % request.user.id)
        form = forms.Login(request)
        return render(request, 'blog/login.html', {'form': form})
    else:
        form = forms.Login(request, request.POST, request.FILES)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    session = request.POST.get('logrecord')
                    if session:
                        request.session.set_expiry(259200)
                return redirect('/home/%s.html' % user.id)
            else:
                form = forms.Login(request, request.POST)
                msg = '用户名或密码错误'
                return render(request, 'blog/login.html', {'form': form, 'msg': msg})
        return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    '''
    退出登录状态
    :param request:
    :return:
    '''
    logout(request)
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


def change_pwd(request):
    """
    修改密码
    :param request:
    :return:
    """
    pass


def home(request,id):
    """
    个人主页,展示个人详细信息
    :return:
    """
    user = models.UserInfo.objects.filter(id=id).first()
    return render(request,'blog/home.html',{'user':user})


@login_required
def blog_register(request,):
    """
    博客注册
    :param request:
    :return:
    """
    if request.method =='GET':
        form = forms.Blog(request)
        return render(request,'blog/blog_register.html',{"form":form})
    else:
        form = forms.Blog(request,request.POST)
        if form.is_valid():
            blogname = form.cleaned_data.get('blogname')
            data = models.BlogInfo.objects.filter(blogname=blogname)
            if not data:
                user = models.UserInfo.objects.filter(id=request.user.id).first()
                models.BlogInfo.objects.create(blogname=blogname,user=user)
                return redirect('/blog/{}/'.format(blogname))
            else:
                msg = '账号已被注册'
                return render(request,'blog/blog_register.html',{"form":form,"msg":msg})
        return render(request, 'blog/blog_register.html', {"form": form})


def blog(request,blogname):
    """
    博客主页
    :param request:
    :param param:
    :return:
    """
    if request.method == 'GET':
        data = models.BlogInfo.objects.filter(blogname=blogname).first()
        if not data :
            return render(request,'blog/404.html')
        return render(request,'blog/blog.html',{'blogname':blogname})

@login_required
def posts(request):
    """
    博客管理后台
    :param request:
    :return:
    """
    return render(request,'blog/posts.html')

@login_required
def editor(request):
    """
    博客编辑页面
    :param request:
    :return:
    """
    if request.method=='GET':
        return render(request,'blog/blogedit.html')





urlpatterns=[
    url(r'^register\.html$',register),
    url(r'^check_code/',check_code),
    url(r'^login\.html$',user_login),
    url(r'^home/(\d+)\.html$',home),
    url(r'^logout\.html$',user_logout),
    url(r'^retrieve\.html$',retrieve),
    url(r'^blogregister/(\d+)\.html$',blog_register),
    url(r'^blog/(.*)/$',blog),
    url(r'^posts$',posts),
    url(r'^editor$',editor),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+[url(r'',index)]







