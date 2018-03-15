# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserInfo(User):
    """
    用户信息表
    """
    nickname = models.CharField(verbose_name='昵称',max_length=32, null=True)
    phone = models.CharField(verbose_name='手机',max_length=11, null=True)
    avatar = models.ImageField(verbose_name='头像',upload_to='img', null=True)
    fans = models.ManyToManyField(verbose_name='粉丝', to='UserInfo', related_name='f')

    def __str__(self):
        return 'id{}----用户名{}'.format(self.id,self.username)


class UserFans(models.Model):
    """
    粉丝关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo',  related_name='users', null=True)
    followers = models.ForeignKey(verbose_name='粉丝', to='UserInfo', related_name='followers', null=True)

    class Meta:
        unique_together = [
            ('user', 'followers'),
        ]
    def __str__(self):
        return '博主{}------粉丝{}'.format(self.user.username,self.followers.username)


class BlogInfo(models.Model):
    """
    博客信息表
    """
    blogname = models.CharField(verbose_name='博客名称',max_length=32, null=True)
    rgtime = models.DateTimeField(verbose_name='注册时间',auto_now_add=True, null=True)
    blogmodel = models.ForeignKey(verbose_name='博客模板',to='BlogModel',default=1)
    user = models.OneToOneField(verbose_name='博客主人',to='UserInfo',  null=True)

    def __str__(self):
        return '博客名{}-------博主账号{}'.format(self.blogname,self.user.username)


class BlogArticleInfo(models.Model):
    """
    博客文章信息表
    """
    blog = models.ForeignKey(verbose_name='所属博客', to='BlogInfo', null=True)
    title = models.CharField(verbose_name='文章标题', max_length=128, null=True)
    summary = models.CharField(verbose_name='文章简介', max_length=255, null=True)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='发表时间',auto_now_add=True, null=True)
    category = models.ForeignKey(verbose_name='文章类型', to="Category", null=True)

    def __str__(self):
        return '博客名{}----文章标题{}'.format(self.blog.blogname,self.title)


class Category(models.Model):
    """
    个人文章分类表
    """
    title = models.CharField(verbose_name='分类标题', max_length=32, null=True,unique=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='BlogInfo', null=True)

    def __str__(self):
        return '分类标题 {}----博客名{}'.format(self.title,self.blog.blogname)


class BlogArticle(models.Model):
    """
    博客文章表
    """
    aid = models.OneToOneField(verbose_name='文章信息',to='BlogArticleInfo', null=True)
    article = models.TextField(verbose_name='文章内容', null=True)

    def __str__(self):
        return '{}'.format(self.aid.title)


class Comment(models.Model):
    """
    评论表
    """
    article = models.ForeignKey(verbose_name='评论文章',to='BlogArticleInfo', null=True)
    father = models.ForeignKey(verbose_name='上级评论',to='Comment',null=True)
    user = models.ForeignKey(verbose_name='评论用户',to='UserInfo', null=True)
    content = models.TextField(verbose_name='评论内容', null=True)
    time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True, null=True)

    def __str__(self):
        return '评论者{} ----评论文章{}'.format(self.user.username,self.article.title)


class BlogModel(models.Model):
    """
    博客模板表
    """
    blogmodelname = models.CharField(verbose_name='模板名称',max_length=16,null=True)
    blogmodel = models.TextField(verbose_name='模板内容', null=True)
    def __str__(self):
        return '{}'.format(self.blogmodelname)
