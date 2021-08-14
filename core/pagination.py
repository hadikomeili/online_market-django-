from rest_framework.pagination import CursorPagination


class APIViewPagination(CursorPagination):
    ordering = '-id'