from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


# Connect admin
admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

# Define debug-mode URLs
# static urls will be disabled in production mode,
# forcing user to configure httpd
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s(.*)$'%settings.MEDIA_URL[1:],
            'django.views.static.serve',
            dict(document_root=settings.MEDIA_ROOT)
        ),
        url(r'^%s(.*)$'%settings.STATIC_URL[1:],
            'django.views.static.serve',
            dict(document_root=settings.STATIC_ROOT)
        ),
    )

    # cms static media
    if 'cms' in settings.INSTALLED_APPS:
        try:
            urlpatterns += patterns('',
                url(r'^%s(.*)$'%settings.CMS_MEDIA_URL[1:],
                    'django.views.static.serve',
                    dict(document_root=settings.CMS_MEDIA_ROOT)
                ),
            )
        except ImportError: pass
