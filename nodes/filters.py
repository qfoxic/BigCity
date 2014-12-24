from rest_framework import filters


#TODO. Add tests for test search categories nodes.
class CategoryFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(parent=request.GET.get('parent'))
