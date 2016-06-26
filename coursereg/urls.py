from django.conf.urls import url
from . import views

app_name = 'coursereg'
urlpatterns = [
    url(r'^signin/$', views.user.signin, name='signin'),
    url(r'^signout/$', views.user.signout, name='signout'),
    url(r'^changepasswd/$', views.user.change_passwd, name='change_passwd'),

    url(r'^fatal/$', views.common.fatal_error, name='fatal'),
    url(r'^faq/$', views.common.faq, name='faq'),
    url(r'^profile/$', views.common.profile, name='profile'),
    url(r'^$', views.common.index, name='index'),

    url(r'^participants/create$', views.participants.create, name='participants_create'),
    url(r'^participants/([0-9]+)/update$', views.participants.update, name='participants_update'),
    url(r'^participants/([0-9]+)/delete$', views.participants.delete, name='participants_delete'),

    url(r'^notifications/dismiss$', views.notifications.dismiss, name='notifications_dismiss'),
    url(r'^notifications/create$', views.notifications.notify, name='notify'),

    url(r'^dcc/([0-9]+)$', views.dcc.students_read, name='dcc_students_read'),
    url(r'^dcc/([0-9]+)/approve$', views.dcc.approve, name='dcc_approve'),


]
