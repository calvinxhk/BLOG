from django.db import models


class User(models.Model):
    uid = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='账号',max_length=32,null=True)
    nickname = models.CharField(verbose_name='昵称',max_length=32,null=True)
    pwd = models.CharField(verbose_name='密码',max_length=64,null=True)
    phone = models.CharField(verbose_name='手机',max_length=11,null=True)
    rg_time = models.DateTimeField(verbose_name='注册时间',auto_now_add=True)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像',upload_to='img')
    blogname = models.OneToOneField(to='BlogInfo')
    fans = models.ManyToManyField(verbose_name='粉丝', to='User', related_name='f')
    class Meta:
        db_table = 'ImageStore'


class UserFans(models.Model):
    """
    粉丝关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='User', to_field='uid', related_name='users')
    followers = models.ForeignKey(verbose_name='粉丝', to='User', to_field='uid', related_name='followers')

    class Meta:
        unique_together = [
            ('user', 'followers'),
        ]

class BlogInfo(models.Model):
    blogname = models.CharField(max_length=32,null=True)
    rgtime = models.CharField(max_length=32,null=True)
    blogmodel = models.ForeignKey('BlogModel',null=True)


class BlogArticleInfo(models.Model):
    blog = models.ForeignKey('BlogInfo',null=True)
    puttime = models.CharField(max_length=32,null=True)
    sort = models.CharField(max_length=32,null=True)


class BlogArticle(models.Model):
    aid = models.OneToOneField('BlogArticleInfo')
    article = models.FileField()

class Comment(models.Model):
    article = models.ForeignKey('BlogArticleInfo',null=True)
    father = models.ForeignKey('Comment',null=True)
    user = models.ForeignKey('User',null=True)
    content = models.CharField(max_length=512,null=True)
    time = models.CharField(max_length=32,null=True)


class Like(models.Model):
    article = models.ForeignKey('BlogArticleInfo',null=True)
    user = models.ForeignKey('User',null=True)

class BlogModel(models.Model):
    blogmodelname = models.CharField(max_length=16,null=True)
    blogmodel = models.FileField()