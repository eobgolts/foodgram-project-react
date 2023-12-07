from rest_framework.routers import DefaultRouter

from authors.views import CustomUserViewset

router = DefaultRouter()

router.register('users/', CustomUserViewset)

urlpatterns = router.urls
