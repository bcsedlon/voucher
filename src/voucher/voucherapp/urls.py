from django.conf.urls import url, include

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^logfile/$', views.logfile, name='logfile'),
    url(r'^simulate/$', views.simulate, name='simulate'),
    url(r'^upload/$', views.upload, name='upload'),
]

