from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet, RecipeViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = router.urls
