from django.contrib import admin
from django.urls import (
    path,
    include
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/users/', include('authors.urls')),
    path('api/', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
