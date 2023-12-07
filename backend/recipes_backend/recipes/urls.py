from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet

router = DefaultRouter()

router.register('tags/', TagViewSet)


urlpatterns = router.urls
