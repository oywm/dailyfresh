from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^index', views.index),
    re_path(r'^list(\d+)_(\d+)_(\d+)/$', views.list1),
    re_path(r'^(\d+)/$', views.detail),
]
