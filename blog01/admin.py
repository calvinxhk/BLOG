from django.contrib import admin
from blog01.models import *

admin.site.register(UserInfo)
admin.site.register(UserFans)
admin.site.register(BlogInfo)
admin.site.register(BlogArticleInfo)
admin.site.register(Category)
admin.site.register(BlogArticle)
admin.site.register(Comment)
admin.site.register(BlogModel)