from rest_framework import pagination


class ScrollPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 100
    page_size_query_param = 'page_size'
