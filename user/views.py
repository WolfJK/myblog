# encoding =utf8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import View
from user import models as model
from django.core.paginator import Paginator
from django.conf import settings
import time, datetime
from django.contrib import auth
# Create your views here.
import os, re
import logging
from django.contrib.auth.decorators import login_required


# file = open('./remain/%s' % 'log001.txt', encoding='utf-8', mode='a')
logger = logging.getLogger(__name__)

logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(filename)s] [line:%(lineno)d] %(levelname)s \n %(message)s',
            datefmt='[%d/%b/%Y %H:%M:%S]',
            # stream=file
            # filename='./remain/%s' % 'log001.txt', filemode='a'
        )


class IndexView(View):
    def get(self, request, *args, **kwargs):
        print(request.METHOD)
        HttpResponse('templates/user/login.html')

    def post(self, request, *args, **kwargs):
        print(request.POST.get('user'))


def page_def(obj, page=1):
    '''分页'''
    logger.info('page_def()')
    PAGE_NUM = 5  # 每页显示 5 条数据
    paginator = Paginator(obj, PAGE_NUM)
    if page > paginator.num_pages:
        page = paginator.num_pages
    if page < 1:
        page = 1
    st = ''
    p_range = list(paginator.page_range)
    page_index = p_range.index(page)
    a = p_range[:5] if p_range.index(page) < 0 else p_range[page-2:page+2]  # 最多显示 5 个按钮
    b = p_range[-1] if p_range.index(page)+2 < p_range[-1] else page_index+2 # 最多显示 5 个按钮
    pages = p_range[:5]
    if len(p_range) > 5:
        if page < p_range[2]:
            pages = p_range[:5]
        elif page > p_range[-3]:
            pages = p_range[-5:]
        else:
            pages = p_range[page-2:page+2]
    print(pages, page, '----', a, b, 's==============')
    for p in pages:
        cu_pa = '<a href="javascript:" class="pageginator page-item" style="color:blue;" page="{p}">第{p}页</a>'.format(p=p)
        if p == page:
            st = st + cu_pa
        else:
            st = st + '<a href="javascript:" class="pageginator page-item" page="{p}">第{p}页</a>'.format(p=p)
    if page > pages[0]:
        st = '<a href="javascript:" class="pageginator" page="{p}">上一页</a>'.format(p=page-1) + st
    if page < pages[-1]:
        st = st + '<a href="javascript:" class="pageginator" page="{p}">下一页</a>'.format(p=page+1)
    print(st)
    return paginator.page(page), st  # page  当前页的对象，页码范围，当前页


# /index
def index(request):
    '''首页'''
    logger.info('/index()')
    print('*'*10, dir(model))
    result = model.Article.objects.all().order_by('-create_at')
    curr_data, page_data = page_def(result)
    recommend_data = ''
    name = request.user.username
    return render(request, 'base.html', {'querys': curr_data, 'name': name})


# /searchArticles
def searchArticles(request, page=1):
    '''文章搜索'''
    logger.info('/searchArticles()')
    page = int(request.POST.get('page'))
    keywords = request.POST.get('keyboard')

    result = model.Article.objects.filter(title__contains=keywords).order_by('-create_at')
    print(keywords, len((result)), page)

    curr_data, page_data = page_def(result, page)
    data = ''
    for curr in curr_data:
        h = '''<li> <h3 id="a_title"><a href="/artileDetail/{article_id}">{article_title}</a></h3><div id="a_content" style="overflow:hidden;max-height:100px;">{article_content}</div><i></i></li>'''\
            .format(article_title=curr.title,
                    article_content=curr.content,
                    article_id=curr.id
                    )
        logger.info(h)
        data = data + h
    name = request.user.username

    return JsonResponse({'data':data, 'page_data': page_data, 'name': name})
    # return render(request, 'base.html', {'querys': curr_data, 'pagerange':pagerange, 'cu_page': cu_page, 'h': h})


# /searchRecommend
def searchRecommend(request):
    '''站长推荐'''
    logger.info('/searchRecommend()')
    queryset = model.Article.objects.all().order_by('-reply_count')[:5]
    temp = ''
    for i in queryset:
        temp += '<li><a href="/artileDetail/{article_id}">{title}</a></li>'.format(title=i.title, article_id=i.id)
    temp = '<ul>' + temp +'</ul>'
    return JsonResponse({'data': temp})


# /article_detail
def artileDetail(request, article_id):
    '''article_id: 文章 id 文章详情'''
    qs = model.Article.objects.get(id=int(article_id))
    content_info = dict(publish_date=qs.create_at, author=qs.user, title=qs.title, content=qs.content,
                        like_count=qs.like_count, reply_count=qs.reply_count, article_id=qs.id)  # 文章的详情
    comments = searchComment(request, article_id) # 查询文章的评论用户名，评论内容，评论时间  list
    # return JsonResponse(dict(comments=comments, content_info=content_info))
    return render(request, 'detail.html', {'data': dict(comments=comments, content_info=content_info)})


# /addLike
def addLike(request):
    logger.info('addLike()')
    if request.user.is_authenticated:
        article_id = request.POST.get('article_id')
        print('*' * 10, article_id)
        qs = model.Article.objects.get(id=int(article_id))
        qs.like_count = qs.like_count + 1

        qs.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    else:
        return JsonResponse({'code': 301, 'message': '请先登录'})


# /addComment
def addComment(request):
    '''评论'''
    # 1. 外键数据插入是通过 表实例还是 字段名
    logger.info('addComment()')
    if request.user.is_authenticated:
        logger.info(request.user.username)
        article_id = request.POST.get('article_id')
        a = model.Article.objects.get(id=article_id)
        # 查询  comment表中的外键
        c1 = model.Comment(create_at=lambda :datetime.datetime.fromtimestamp(time.time()),
                       reply_username=request.user.username,
                       reply_content=request.POST.get('reply_content'),
                       article_id=a)
        c1.save()
        arti1 = model.Article.objects.get(id=article_id)  # 回复数 + 1
        arti1.reply_count = arti1.reply_count + 1
        arti1.save()
        logger.info('评论成功')
        return JsonResponse({'code': 200, 'message': 'success'})
    else:
        return JsonResponse({'code': 301, 'message': '请先登录'})


# /searchComment
def searchComment(request, article_id):
    '''查询文章的所有评论'''
    logger.info('searchComment()')
    qs = model.Comment.objects.filter(article_id=int(article_id), ).order_by('-create_at')
    temp = list()
    for comment in qs:
        temp.append(dict(created_at=comment.create_at, reply_name=comment.reply_username, reply_cont=comment.reply_content))
    return dict(detail=temp)


# /register
# def register(request):
#     logger.info('**register()')
#     name = request.POST.get('username')
#     password = request.POST.get('username')
#     confirm_password = request.POST.get('username')
#     email = request.POST.get('email')
#     error_msg = dict(code=0, msg='')
#     if not all([name, password, confirm_password]):
#         error_msg['msg'] = '请输入用户名或密码'
#         return error_msg
#
#     if password.strip() != confirm_password.strip():
#         error_msg['msg'] = '密码和确认密码不一致'
#         return error_msg
#
#     if not email:
#         return error_msg
#
#     user = model.MyUser.objects.create_user(username=name, password=password, email=email)
#     user.save()
#



class RegisterView(View):
    def get(self, request):

        return render(request, 'user/register.html', context=None)


    def post(self, request):
        logger.info(dir(request))
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        error_msg = dict(code=0, msg='注册成功')
        gender = request.POST.get('gender')
        print('*'*10)
        print(username, password, email, tel, confirm_password, gender)
        if not all([username, password, confirm_password]):
            error_msg['msg'] = '请输入用户名或密码'
            error_msg['code'] = 1
            return JsonResponse(error_msg)

        if password.strip() != confirm_password.strip():
            error_msg['msg'] = '密码和确认密码不一致'
            error_msg['code'] = 1
            return JsonResponse(error_msg)

        # if not re.search('^[1][3-8][0-9]{9}$', tel):
        #     error_msg['msg'] = '手机号不符合规则'
        #     error_msg['code'] = 1
        #     return JsonResponse(error_msg)

        if not email:
            error_msg['msg'] = '请填写邮箱'
            error_msg['code'] = 1
            return JsonResponse(error_msg)
            # return render(request, 'user/register.html', {'data': error_msg})
        logger.info(error_msg)
        if model.MyUser.objects.filter(username=username):
            error_msg['msg'] = '用户已存在'
            error_msg['code'] = 1
            return JsonResponse(error_msg)
        user = model.MyUser.objects.create_user(username=username, password=password, email=email, mobile=tel, )
        user.save()
        return JsonResponse(error_msg)
        # return HttpResponseRedirect('/login')
        # return render(request, 'user/login.html', {'data': error_msg})


# /login
class LoginView(View):
    def get(self, request):

        return render(request, 'user/login.html', context=None)


    def post(self, request):
        logger.info('LoginView.post()')
        user = request.POST.get('username', '')
        pwd = request.POST.get('password', '')

        us = auth.authenticate(request, username=user, password=pwd)
        msg = {'code': 0, 'msg': '登录成功'}
        print('='*10, user, pwd, us)
        if not all([user, pwd]):
            msg['code'] = 1
            msg['msg'] = '请输入用户名或密码'
            return JsonResponse(msg)
        if us and us.is_active:
            logger.info(msg)
            auth.login(request, us)
            msg['name'] = request.user.username
            return JsonResponse(msg)
        else:
            msg['code'] = 1
            msg['msg'] = '用户名或密码错误'
            return JsonResponse(msg)


# /logout
def logout(request):
    logger.info('logout')
    auth.logout(request)
    msg = {'code': 0, 'msg': '登出成功'}
    return HttpResponseRedirect('/index')
