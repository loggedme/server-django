from typing import Any, Dict, Iterable, Union

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SimplePagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'

    def get_paginated_response(self, data: Iterable[Union[Dict, Any]]):
        return Response({
            'count': self.page.paginator.count,
            'is_countable': True,
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'items': data,
        })


simple_pagination = SimplePagination()
