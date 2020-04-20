from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from user import models
from django.core.paginator import Paginator
from django.conf import settings
import time, datetime
# Create your views here.
import logging

logging.basicConfig(format='%(asctime)s %[(filename)]s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        print(request.METHOD)
        HttpResponse('templates/user/login.html')

    def post(self, request, *args, **kwargs):
        print(request.POST.get('user'))


def page_def(obj, page=1):
    '''分页'''
    logger.info('page_def()')
    PAGE_NUM = 3  # 每页显示 5 条数据
    paginator = Paginator(obj, PAGE_NUM)
    if page > paginator.num_pages:
        page = paginator.num_pages
    if page < 1:
        page = 1
    st = ''
    p_range = list(paginator.page_range)
    page_index = p_range.index(page)
    a = p_range[:5] if p_range.index(page) < 0 else p_range[page-2:page+2] # 最多显示 5 个按钮
    b = p_range[-1] if p_range.index(page)+2 < p_range[-1] else page_index+2# 最多显示 5 个按钮
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
    logger.info('/index()--><--')
    print('--><--', settings.STATICFILES_DIRS, settings.BASE_DIR)
    result = models.Article.objects.all().order_by('-create_at')
    curr_data, page_data = page_def(result)
    recommend_data = ''
    return render(request, 'base.html', {'querys': curr_data})


# /searchArticles
def searchArticles(request, page=1):
    '''文章搜索'''
    logger.info('/searchArticles()')
    page = int(request.POST.get('page'))
    keywords = request.POST.get('keyboard')

    result = models.Article.objects.filter(article_title__contains=keywords).order_by('-create_at')
    print(keywords, len((result)), page)

    curr_data, page_data = page_def(result, page)
    data = ''
    for curr in curr_data:
        h = '''<li> <h3 id="a_title"><a href="/artileDetail/{article_id}">{article_title}</a></h3><p id="a_content">{article_content}</p><i></i></li>'''\
            .format(article_title=curr.article_title,
                    article_content=curr.article_content,
                    article_id=curr.id
                    )
        data = data + h
    return JsonResponse({'data':data, 'page_data': page_data})
    # return render(request, 'base.html', {'querys': curr_data, 'pagerange':pagerange, 'cu_page': cu_page, 'h': h})


# /searchRecommend
def searchRecommend(request):
    '''站长推荐'''
    logger.info('/searchRecommend()')
    queryset = models.Article.objects.all().order_by('-reply_count')[:5]
    temp = ''
    for i in queryset:
        temp += '<li><a href="/artileDetail/{article_id}">{title}</a></li>'.format(title=i.article_title, article_id=i.id)
    temp = '<ul>' + temp +'</ul>'
    return JsonResponse({'data': temp})


# /article_detail
def artileDetail(request, article_id):
    '''article_id: 文章 id 文章详情'''
    qs = models.Article.objects.get(id=int(article_id))
    content_info = dict(publish_date=qs.create_at, author=qs.user_id, title=qs.article_title, content=qs.article_content,
                        like_count=qs.like_count, reply_count=qs.reply_count, article_id=qs.id)  # 文章的详情
    comments = searchComment(request, article_id) # 查询文章的评论用户名，评论内容，评论时间  list
    print(comments)
    # return JsonResponse(dict(comments=comments, content_info=content_info))
    return render(request, 'detail.html', {'data':dict(comments=comments, content_info=content_info)})


# /addLike
# def addLike(request, article_id):
#     logger.info('addLike()----<><><>')
#     qs = models.Article.objects.get(id=int(article_id))
#     qs.like_count = qs.like_count + 1
#     print(article_id)
#     input('----------------')
#     qs.save()
#     return JsonResponse({'message': 'success'})


# /addComment
def addComment(request):
    '''评论'''
    article_id = request.POST.get('article_id')
    # 查询  comment表中的外键
    c1 = models.Comment(create_at=lambda :datetime.datetime.fromtimestamp(time.time()),
                   reply_username=request.POST.get('reply_name'),
                   reply_content=request.POST.get('reply_content'),
                   article_id=request.POST.get('article_id'))
    c1.save()
    arti1 = models.Article.objects.get(id=article_id)  # 回复数 + 1
    arti1.reply_count = arti1.reply_count + 1
    arti1.save()
    return JsonResponse({'message': 'success'})


# /searchComment
def searchComment(request, article_id):
    '''查询文章的所有评论'''
    logger.info('searchComment()')
    qs = models.Comment.objects.filter(article_id=int(article_id), ).order_by('-create_at')
    temp = list()
    for comment in qs:
        temp.append(dict(created_at=comment.create_at, reply_name=comment.reply_username, reply_cont=comment.reply_content))
    return dict(detail=temp)


