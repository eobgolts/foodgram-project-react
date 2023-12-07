from django.urls import (
    re_path,
    include
)
from rest_framework.routers import DefaultRouter
from authors.views import CustomUserViewset

router = DefaultRouter()

router.register('', CustomUserViewset)

urlpatterns = [
    re_path('users/', include(router.urls)),
]
