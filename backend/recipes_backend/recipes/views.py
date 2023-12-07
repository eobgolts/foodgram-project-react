from rest_framework import (
    viewsets,
    permissions,
)

from recipes.models import Tag
from recipes.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    model = Tag
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
