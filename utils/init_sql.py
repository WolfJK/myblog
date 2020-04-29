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
    u = models.User(username='管理员', password='aaaa1111', is_active=1,
                    is_staff=1, is_superuser=1, email='abc@qq.com', first_name='a',
                last_name='b', date_joined=datetime.datetime.now())
    u.save()
    a = models.Article(user=u, article_title='title', article_content='content', reply_count=10, like_count=21)
    a.save()


def select():
    # 初始化数据库

    a = models.Article.objects.all()
    print(a)


if __name__ == '__main__':
    print(pwd)
    # migrate()
    # insertData()
    select()