from rest_framework import pagination


def get_pagination_class_with_size(_page_size=10):
    class CustomPaginationWithSize(pagination.PageNumberPagination):
        page_size = _page_size

        def get_paginated_response(self, data):
            response = super(CustomPaginationWithSize, self).get_paginated_response(data)
            response.data['total_pages'] = self.page.paginator.num_pages
            return response

    return CustomPaginationWithSize
