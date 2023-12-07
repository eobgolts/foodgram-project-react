from rest_framework.routers import DefaultRouter

from ingredients.views import IngridientViewSet

router = DefaultRouter()

router.register('', IngridientViewSet)

urlpatterns = router.urls
