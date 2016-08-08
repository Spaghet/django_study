from django.conf.urls import url

from . import views

app_name = "polls"

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^(?P<question_id>[09iw_]+)/results/$', views.results, name="results"),
    url(r'^(?P<question_id>[09iw_]+)/vote/$', views.vote, name="vote"),
]
