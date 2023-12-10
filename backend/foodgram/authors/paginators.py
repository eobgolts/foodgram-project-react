from rest_framework.pagination import (
    PageNumberPagination,
)


class CustomAuthorPagination(PageNumberPagination):
    page_size_query_param = 'limit'
