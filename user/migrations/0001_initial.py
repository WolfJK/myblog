# Generated by Django 2.0 on 2020-04-29 17:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=20, unique=True, verbose_name='用户名')),
                ('email', models.EmailField(max_length=120, verbose_name='邮箱')),
                ('mobile', models.CharField(default='', max_length=11, verbose_name='手机')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', null=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(help_text='删除时间', null=True, verbose_name='删除时间')),
                ('title', models.CharField(help_text='文章的标题', max_length=120, verbose_name='文章的标题')),
                ('content', models.TextField(help_text='文章的正文', verbose_name='文章的正文')),
                ('reply_count', models.IntegerField(default=0, help_text='评论数', verbose_name='评论数')),
                ('like_count', models.IntegerField(default=0, help_text='点赞数', verbose_name='点赞数')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL, verbose_name='文章发表用户名')),
            ],
            options={
                'verbose_name': 'article',
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='更新时间', null=True, verbose_name='更新时间')),
                ('delete_at', models.DateTimeField(help_text='删除时间', null=True, verbose_name='删除时间')),
                ('reply_username', models.CharField(help_text='评论的用户名', max_length=64, verbose_name='评论的用户名')),
                ('reply_content', models.TextField(help_text='评论内容', verbose_name='评论内容')),
                ('article', models.ForeignKey(help_text='文章的id', on_delete='models.CASCADE', to='user.Article', verbose_name='文章的id')),
            ],
            options={
                'verbose_name': 'comment',
                'db_table': 'comment',
            },
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['article'], name='comment_article_56e73b_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['user', 'title'], name='article_user_id_9fbe7e_idx'),
        ),
    ]
