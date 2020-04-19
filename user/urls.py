from django.urls import path, include
from user import views
from django.conf.urls import url

app_name = 'user'

urlpatterns = [
    # path('index', views.IndexView.as_view(), name='index'),
    url(r'^index$', views.index, name='index'),
    # url(r'index\?(?P<page>page=(\d+))', views.index, name='index'),
    url(r'^searchArticles$', views.searchArticles, name='searchArticles'),  # 查询文章
    url(r'^searchRecommend$', views.searchRecommend, name='searchRecommend'),  # 查询站长推荐内容
    url(r'^artileDetail/(?P<article_id>\d+)$', views.artileDetail, name='artileDetail'),
    url(r'^searchComment$', views.searchComment, name='searchComment'),
    url(r'^addComment$', views.addComment, name='addComment'),
    # url(r'^addLike\?(?P<article_id>article_id=\d+)$', views.addLike, name='addLike'),
    # url(r'searchLike', views.searchLike, name='searchLike'),
    url(r'^$', views.index, name='index'),
]
