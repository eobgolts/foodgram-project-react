from django.urls import (
    path,
    re_path,
    include
)
from rest_framework.routers import DefaultRouter
from authors.views import SubscriptionListViewSet

router = DefaultRouter()


#router.register(r'^(?P<author_id>\d+)/subscribe/', SubscriptionListViewSet, basename='subscription')
router.register(r'subscriptions\/$', SubscriptionListViewSet, basename='subscriptions')

urlpatterns = [
    re_path(r'subscriptions\/$', include(router.urls))
]
