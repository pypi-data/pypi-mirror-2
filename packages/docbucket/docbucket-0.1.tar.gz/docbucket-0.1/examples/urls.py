import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'', include('docbucket.urls')),
)
