from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    def dispatch(self, request, *args, **kwargs):
        self.manager = self.manager_class(request)
        return super(BaseViewSet, self).dispatch(request, *args, **kwargs)
