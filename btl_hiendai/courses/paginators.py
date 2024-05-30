from rest_framework import pagination


class PaymentPaginator(pagination.PageNumberPagination):
    page_size = 5


class PackagePaginator(pagination.PageNumberPagination):
    page_size = 5
