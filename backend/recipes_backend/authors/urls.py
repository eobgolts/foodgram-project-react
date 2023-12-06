from django.urls import (
    path,
    re_path,
    include
)
from rest_framework.routers import DefaultRouter
from authors.views import SubscriptionListViewSet, SubscriptionViewSet

router = DefaultRouter()

router.register('(?P<user_id>\d+)/subscribe/', SubscriptionViewSet, basename='subscription')
#router.register(r'', SubscriptionListViewSet, basename='subscriptions')

urlpatterns = [
    re_path('api/users/', include(router.urls))
]
