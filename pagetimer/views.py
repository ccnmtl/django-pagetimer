import csv

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.views.generic.list import ListView

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
class DashboardView(ListView):
    template_name = "pagetimer/dashboard.html"
    model = PageVisit


# TODO: superuser-only
class CSVView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=pagevisits.csv'

        writer = csv.writer(response)
        writer.writerow(['timestamp', 'username', 'session_key', 'ipaddress',
                         'path'])
        # for CSV, I think we actually want chronological order instead of
        # reverse-chron
        for pv in PageVisit.objects.all().order_by('visited'):
            writer.writerow([
                pv.visited, pv.username, pv.session_key, pv.ipaddress, pv.path,
            ])

        return response
