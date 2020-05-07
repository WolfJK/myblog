import sys, os
import django
import datetime
pwd = os.path.dirname(os.path.realpath(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")

django.setup()  # 初始化django路径

from user import models

# f = models.Article.objects.all()
# print([_.article_title + _.article_content for _ in f])

def migrate():
    # 执行迁移文件
    print(os.popen('python ../manage.py makemigrations').read())
    print(os.popen('python ../manage.py migrate').read())


def insertData():
    # 初始化数据库
    u = models.MyUser(username='管理员', password='aaaa1111', is_active=1,
                    is_staff=1, is_superuser=1, email='abc@qq.com', first_name='a',
                last_name='b', date_joined=datetime.datetime.now(), mobile='18221278748')
    u.save()
    a = models.Article(user=u, title='自定义 Django 中的认证机制',
                       content='''指定身份认证后端 :
                       在幕后，Django 维护着一个 “身份认证后端” 列表，用于检查身份认证,
在 AUTHENTICATION_BACKENDS setting 中指定要使用的身份验证后端列表。''',
                       reply_count=10, like_count=21)
    a.save()


def select():
    # 初始化数据库

    a = models.Article.objects.all()
    print(a)


if __name__ == '__main__':
    print(pwd)
    # migrate()
    insertData()
    select()