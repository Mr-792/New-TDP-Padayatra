from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):

    # def get_paginated_response(self, data):
    #     return Response({
    #         'links': {
    #            'next': self.get_next_link(),
    #            'previous': self.get_previous_link()
    #         },
    #         'count': self.page.paginator.count,
    #         'total_pages': self.page.paginator.num_pages,
    #         'results': data
    #     })

    def get_paginated_response(self, data):
        return Response({
            'message':'Fetched successfully.',
            'count': self.page.paginator.num_pages,
            'data': data
        })