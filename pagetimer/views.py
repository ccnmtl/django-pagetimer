from django.http import JsonResponse
from django.views.generic.base import View, TemplateView

from .models import PageVisit


class PageTimerEndpointView(View):
    def post(self, request):
        username = request.user.username
        session_key = request.session.session_key
        path = request.POST["path"]
        ipaddress = request.META.get(
            'HTTP_X_FORWARDED_FOR',
            request.META.get(
                'REMOTE_ADDR', "none"
            )
        )
        PageVisit.objects.log_visit(
            username,
            session_key,
            path,
            ipaddress,
        )
        return JsonResponse({"status": "ok"})


# TODO: superuser-only
class DashboardView(TemplateView):
    template_name = "pagetimer/dashboard.html"
