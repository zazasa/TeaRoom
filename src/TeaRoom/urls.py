from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
import courses.urls
import uploader.urls
from . import views

# Links URLs to views
urlpatterns = patterns(
    '',
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^', include(accounts.urls, namespace='accounts')),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(courses.urls, namespace='courses')),
    url(r'^', include(uploader.urls, namespace='uploader')),
    url(r'^help/$', views.HelpView.as_view(), name="help"),
)

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
