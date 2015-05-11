from django.conf.urls import patterns, url

from . import views
urlpatterns = patterns('',
                       url(r'^login/$', views.LoginView.as_view(), name="login"),
                       url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
                       url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
                       url(r'^signup-complete/$', views.SignUpCompleteView.as_view(), name='signup-complete'),
                       url(r'^password-change/$', views.PasswordChangeView.as_view(),
                           name='password-change'),
                       url(r'^password-reset/$', views.PasswordResetView.as_view(),
                           name='password-reset'),
                       url(r'^password-reset-done/$', views.PasswordResetDoneView.as_view(),
                           name='password-reset-done'),
                       url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$$', views.PasswordResetConfirmView.as_view(),
                           name='password-reset-confirm'),
                       url(r'^first-password-set-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$$', views.FirstPasswordSetConfirmView.as_view(), name='first-password-set-confirm'),
                       url(r'^first-password-set-done/$', views.FirstPasswordSetDoneView.as_view(),
                           name='first-password-set-done'),
                       )
