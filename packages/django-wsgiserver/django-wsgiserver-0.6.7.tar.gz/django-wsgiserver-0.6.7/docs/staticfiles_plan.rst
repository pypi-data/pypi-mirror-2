With django 1.3, there will be more support for static files based on
incorporating django-static files into django.contrib.  This is great and it
should make it possible to automatically deploy django apps with the wsgiserver.



a new settings parameter

{{STATICFILES_URL}}

django.contrib.staticfiles is being added
STATICFILES_DIRS
STATICFILES_FINDERS
STATICFILES_ROOT

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
