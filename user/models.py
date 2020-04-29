from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

# Create your models here.
from utils.db import CommonModels
# class MyUser(AbstractUser):
#     username = models.CharField(help_text='用户名', verbose_name='用户名', max_length=64)
#     password = models.CharField(null=False, help_text='密码', verbose_name='密码', max_length=64)
#     tel = models.CharField(null=False, unique=True, help_text='手机号', verbose_name='手机号', max_length=11)
#     is_admin = models.IntegerField(default=0, help_text='1：管理员', verbose_name='是否是管理员',)
#     id_locked = models.IntegerField(default=0, help_text='是否锁定;0 未被锁定', verbose_name='是否锁定')
#     is_delete = models.IntegerField(default=0, help_text='是否被删除;0 未被删除', verbose_name='是否被删除')
#
#     class Meta:
#         verbose_name = 'user'
#         db_table = 'user'


class MyUser(AbstractUser):
    username = models.CharField(max_length=20, verbose_name='用户名',
                                unique=True,
                                help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                },
                                )
    # password = models.CharField(max_length=120, verbose_name='密码')
    email = models.EmailField(max_length=120, verbose_name='邮箱')
    mobile = models.CharField(max_length=11, verbose_name='手机', default='')

    class Meta:
        db_table = 'user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Article(CommonModels):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='文章发表用户名', on_delete='models.CASCADE')
    title = models.CharField(max_length=120, help_text='文章的标题', verbose_name='文章的标题')
    content = models.TextField(help_text='文章的正文', verbose_name='文章的正文')
    reply_count = models.IntegerField(default=0, help_text='评论数', verbose_name='评论数')
    like_count = models.IntegerField(default=0, help_text='点赞数', verbose_name='点赞数')

    class Meta:
        verbose_name = 'article'
        db_table = 'article'
        indexes = [models.Index(fields=['user', 'title']), ]


class Comment(CommonModels):
    article = models.ForeignKey('Article', help_text='文章的id', verbose_name='文章的id', on_delete='models.CASCADE')
    reply_username = models.CharField(max_length=64, help_text='评论的用户名', verbose_name='评论的用户名')
    reply_content = models.TextField(help_text='评论内容', verbose_name='评论内容')

    class Meta:
        verbose_name = 'comment'
        db_table = 'comment'
        indexes = [models.Index(fields=['article', ])]