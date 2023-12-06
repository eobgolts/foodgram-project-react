from django.contrib import admin
from django.urls import (
    path,
    re_path,
    include
)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/users/.*bscri.*', include('authors.urls')),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
