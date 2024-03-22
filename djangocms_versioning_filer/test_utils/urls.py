from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.static import serve


try:
    from django.views.i18n import JavaScriptCatalog
    javascript_catalog = JavaScriptCatalog.as_view()
except ImportError:
    from django.views.i18n import javascript_catalog


admin.autodiscover()

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    re_path(r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog),  # NOQA
    path('', include('filer.server.urls')),
    path('filer/', include('filer.urls')),
]
try:
    i18n_urls = [
        re_path(r'^admin/', admin.site.urls),
    ]
except Exception:
    i18n_urls = [
        path('admin/', include(admin.site.urls)),
    ]

if settings.USE_CMS:
    i18n_urls.append(
        path('', include('cms.urls'))  # NOQA
    )

urlpatterns += i18n_patterns(*i18n_urls)
urlpatterns += staticfiles_urlpatterns()
