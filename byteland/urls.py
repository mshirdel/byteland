from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import index


urlpatterns = [
    path('', index, name='byteland_home'),
    path('admin/', admin.site.urls),
    path('auth/', include('byteland.authentication.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
