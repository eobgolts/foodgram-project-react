from django.contrib import admin
from django.urls import (
    path,
    include
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/users/', include('authors.urls')),
    path('api/', include('recipes.urls')),
]