from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^trigger-500$', 'sentry.tests.views.raise_exc', name='sentry-raise-exc'),
    url(r'^trigger-500-decorated$', 'sentry.tests.views.decorated_raise_exc', name='sentry-raise-exc-decor'),
    url(r'', include('sentry.urls')),
)