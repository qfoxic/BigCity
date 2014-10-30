from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    manager_class = None

    def initial(self, request, *args, **kwargs):
        res = super(BaseViewSet, self).initial(request, *args, **kwargs)
        self.manager = self.manager_class(request) if self.manager_class else None
        return res

