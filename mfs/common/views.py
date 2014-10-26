from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    def initial(self, request, *args, **kwargs):
        res = super(BaseViewSet, self).initial(request, *args, **kwargs)
        self.manager = self.manager_class(request)
        return res

