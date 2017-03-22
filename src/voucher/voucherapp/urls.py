from django.conf.urls import url, include

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    
    url(r'^logfile/$', views.logfile, name='logfile'),
    
    #url(r'^archive/$', views.archive, name='archive'),
 
    url(r'^simulate/$', views.simulate, name='simulate'),
    #url(r'^simulate/(?P<rfid>[0-9]+)/$', views.simulate, name='simulate'),
    url(r'^upload/$', views.upload, name='upload'),
    
    #url(r'^archive/(?P<locationpk>[0-9]+)/(?P<hostpk>[0-9]+)/(?P<maskpk>[0-9]+)/$', views.archive, name='archive'),
    #url(r'^archive/(?P<locationpk>[0-9]+)/(?P<hostpk>[0-9]+)/(?P<maskpk>[0-9]+)/(?P<archivepk>[0-9]+)/$', views.archive, name='archive'),
    
    #url(r'^archive_update/(?P<locationpk>[0-9]+)/$', views.archive_update, name='archive_update'),
    
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login2.html'}, name='login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logged_out2.html'}, name='logout'),
    
    #url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'registration/password_change_form2.html'}, name='password_change'),
    #url(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done',  {'template_name': 'registration/password_change_done2.html'}, name='password_change_done'),
]

