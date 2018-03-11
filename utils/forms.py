from django import forms
from django.forms import Form,fields,widgets
from django.core.exceptions import ValidationError

class Register(Form):
    '''
    用户注册表单验证
    '''
    username = fields.CharField(
        min_length=6,max_length=16,
        error_messages={'required':'用户名不能为空','min_length':'用户名至少6个字符'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    password = fields.CharField(
        max_length=16,min_length=6,
        error_messages={'required':'密码不能为空',"invalid":'不能包含非法字符','min_length':'密码至少6个字符'},
        widget=widgets.PasswordInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    password2 = fields.CharField(
        max_length=16, min_length=6,
        error_messages={'required': '密码不能为空', "invalid": '不能包含非法字符'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))

    nickname=fields.CharField(
        max_length=16,min_length=1,
        error_messages={'required': '昵称不能为空', "invalid": '不能包含非法字符'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    email = fields.EmailField(
        max_length=32,min_length=8,
        error_messages={'required': '邮箱不能为空', "invalid": '请输入正确邮箱'},
        widget=widgets.EmailInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    phone = fields.RegexField(
        '^1\d{10}',
        error_messages={'required': '手机不能为空', "invalid": '请输入正确手机号'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    avatar = fields.FileField(
        widget=widgets.FileInput(attrs={'style':"width:200px;height:200px;opacity:0;position:absolute;top:0"}))

    piccode = fields.CharField(
        error_messages={'required': '验证码不能为空', "invalid": '请输入正确验证码'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    def __init__(self, request, *args, **kwargs):
        """
        引入request参数
        :param request:
        :param args:
        :param kwargs:
        """
        super(Register, self).__init__(*args, **kwargs)
        self.request = request


    def clean_piccode(self):
        inputcode = self.cleaned_data.get('piccode')
        turecode = self.request.session.get('piccode')
        if inputcode == turecode:
            return inputcode
        raise ValidationError('验证码错误')

    def clean_password2(self):
        pwd = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd==pwd2:
            return pwd
        raise ValidationError('两次密码不一致')


class Login(Form):
    '''
    用户登录表单验证
    '''
    username = fields.CharField(
        min_length=4, max_length=16,
        error_messages={'required': '用户名不能为空', 'min_length': '用户名至少6个字符'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))
    password = fields.CharField(
        max_length=16, min_length=6,
        error_messages={'required': '密码不能为空', "invalid": '不能包含非法字符', 'min_length': '密码至少6个字符'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))
    piccode = fields.CharField(
        error_messages={'required': '验证码不能为空', "invalid": '请输入正确验证码'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))

    def __init__(self, request, *args, **kwargs):
        """
        引入request参数
        :param request:
        :param args:
        :param kwargs:
        """
        super(Login, self).__init__(*args, **kwargs)
        self.request = request

    def clean_piccode(self):
        inputcode = self.cleaned_data.get('piccode')
        turecode = self.request.session.get('piccode')
        if inputcode == turecode:
            return inputcode
        raise ValidationError('验证码错误')


class Retrieve(Form):
    '''
    找回密码表单
    '''
    email = fields.EmailField(
        max_length=32, min_length=8,
        error_messages={'required': '邮箱不能为空', "invalid": '请输入正确邮箱'},
        widget=widgets.EmailInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))

    phone = fields.RegexField(
        '^1\d{10}',
        error_messages={'required': '手机不能为空', "invalid": '请输入正确手机号'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))

    name = fields.CharField(
        min_length=6, max_length=16,
        error_messages={'required': '用户名不能为空', 'min_length': '用户名至少6个字符'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))
    piccode = fields.CharField(
        error_messages={'required': '验证码不能为空', "invalid": '请输入正确验证码'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))

    def __init__(self, request, *args, **kwargs):
        """
        引入request参数
        :param request:
        :param args:
        :param kwargs:
        """
        super(Retrieve, self).__init__(*args, **kwargs)
        self.request = request

    def clean_piccode(self):
        inputcode = self.cleaned_data.get('piccode')
        turecode = self.request.session.get('piccode')
        if inputcode == turecode:
            return inputcode
        raise ValidationError('验证码错误')


class Blog(Form):
    """
    博客申请表单
    """
    blogname = fields.CharField(min_length=2,max_length=16,
                            error_messages={'required': '博客名不能为空', 'min_length': '用户名至少6个字符'
                                , "invalid": '博客名只能由字母数字下划线组成'},
                            widget=widgets.TextInput(
                                attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'})
                            )
    piccode = fields.CharField(
        error_messages={'required': '验证码不能为空', "invalid": '请输入正确验证码'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))

    def __init__(self, request, *args, **kwargs):
        """
        引入request参数
        :param request:
        :param args:
        :param kwargs:
        """
        super(Blog, self).__init__(*args, **kwargs)
        self.request = request

    def clean_piccode(self):
        inputcode = self.cleaned_data.get('piccode')
        turecode = self.request.session.get('piccode')
        if inputcode == turecode:
            return inputcode
        raise ValidationError('验证码错误')

    def clean_blogname(self):
        import re
        blogname = self.cleaned_data.get('blogname')
        res = re.match('[a-zA-Z0-9_]+',blogname).group()
        if res == blogname:
            return blogname
        else:
            raise ValidationError('博客名只能由字母数字下划线组成!')



class Article(Form):
    """
    博客发表表单
    """
    title = fields.CharField(min_length=1,max_length=128,
        error_messages={'required':'标题名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))
    summary = fields.CharField(min_length=1,max_length=255,
        error_messages={'required':'简介不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))
    content = fields.CharField(
        error_messages={'required':'分类不能为空'},
        widget=forms.Textarea(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

    def clean_content(self):
        content = self.cleaned_data.get('content')
        from utils.xss import clean
        content = clean(content)
        return content
