from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from events.views import PGEventsView

from .views import MainView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', MainView.as_view(), name='home'),
    # url(r'^otrme/', include('otrme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^events/?$',
        PGEventsView.as_view()),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
