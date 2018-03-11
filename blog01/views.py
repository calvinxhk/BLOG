from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.db import transaction
from django.db.models import F,Count
from io import BytesIO
from blog01 import models
from utils import forms
from utils.piccode import piccode


def index(request):
    """
    主站页面
    :param request:
    :return:
    """
    if request.method =='GET':
        userinfo = models.UserInfo.objects.filter(id=request.user.id).first()#传当前用户信息
        data = models.BlogArticleInfo.objects.all().order_by('create_time')
        category_list = models.BlogArticleInfo.objects.all().values_list('category__title').annotate(number=Count('id'))
        hot_article = models.BlogArticleInfo.objects.all().order_by('read_count')
        hot_blog = models.BlogInfo.objects.all()
        data_dict = {
            "data": data,
            "userinfo": userinfo,
            "category_list": category_list,
            'hot_article': hot_article,
            'hot_blog':hot_blog
        }
        return render(request,'blog/index.html',data_dict)


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
                return redirect('/')
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
    return redirect('/login/')


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
        form = forms.Retrieve(request, request.POST)
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
def blog_register(request):
    """
    博客注册
    :param request:
    :return:
    """
    if request.method =='GET':
        record = models.BlogInfo.objects.filter(user=request.user.id).first()
        if record is not None:
            return redirect('/home/{}'.format(request.user.id))
        form = forms.Blog(request)
        return render(request,'blog/blog_register.html',{"form":form})
    else:
        form = forms.Blog(request, request.POST)
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
    :param blogname:
    :return:
    """
    if request.method == 'GET':
        data = models.BlogInfo.objects.filter(blogname=blogname).first()
        if data is not None:
            return render(request,'blog/blog.html',{'blogname':blogname})
        else:
            return redirect('/404')


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
        blog = models.BlogInfo.objects.filter(user=request.user.id).first()
        category = models.Category.objects.filter(blog=blog).all()
        editor_form = forms.Article()
        return render(request,'blog/blogedit.html',{'editor_form':editor_form,'category':category})
    else:
        editor_form = forms.Article(request.POST, request.FILES)
        if editor_form.is_valid():
            category = request.POST.get('category')
            with transaction.atomic():
                blog = models.BlogInfo.objects.filter(user=request.user.id).first()
                title = editor_form.cleaned_data.get('title')
                summary = editor_form.cleaned_data.get('summary')
                content = editor_form.cleaned_data.get('content')
                category = models.Category.objects.create(title=category, blog=blog)
                aid = models.BlogArticleInfo.objects.create(blog=blog,category=category,title=title,summary=summary)
                models.BlogArticle.objects.create(aid=aid,article=content)
            return render(request,'blog/posts.html',)
        else:
            return render(request,'blog/blogedit.html',{'editor_form':editor_form})


@login_required
def upload(request):
    """
    博客文章中图片上传
    :param request:
    :return:
    """
    if request.method =="POST":
        obj = request.FILES.get('imgFile')
        import os,json,time
        file_path = os.path.join('media/img','%s%s%s'%(request.user.id,time.time(),obj.name))
        with open(file_path,'wb') as f:
            for chunk in obj.chunks():
                f.write(chunk)
        dic = {
            'error':0,
            'url':'/'+file_path,
            'message':'未知错误，请重试！'
        }
        return HttpResponse(json.dumps(dic))


def read(request,*args):
    result =  models.BlogArticleInfo.objects.filter(blog__blogname=args[0],id=args[1])
    content =result.first()
    if content is not None:
        result.update(read_count=F('read_count')+1)
        return render(request,'blog/read.html',{"content":content})
    else:
        return redirect('/404')


def wrong(request):
    """
    404 页面
    :param request:
    :return:
    """
    return render(request,'blog/404.html')


urlpatterns=[
    url(r'^register/$',register),
    url(r'^check_code/',check_code),
    url(r'^login/$',user_login),
    url(r'^home/(\d+)/$',home),
    url(r'^logout/$',user_logout),
    url(r'^retrieve/$',retrieve),
    url(r'^blogregister/$',blog_register),
    url(r'^blog/([a-zA-Z0-9_]+)/$',blog),
    url(r'^read/([a-zA-Z0-9_]+)/(\d+)/$',read),
    url(r'^posts/$', posts),
    url(r'^editor/$', editor),
    url(r'^upload/$', upload), url(r'^$',index)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+[url(r'',wrong)]







