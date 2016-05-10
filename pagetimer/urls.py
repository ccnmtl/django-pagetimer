from django.conf.urls import url

import pagetimer.views as views

urlpatterns = [
    url('^$', views.DashboardView.as_view(
        paginate_by=100,
    ), name='pagetimer-dashboard'),
    url('^csv/$', views.CSVView.as_view(), name='pagetimer-csv'),
    url('^endpoint/$', views.PageTimerEndpointView.as_view(),
        name='pagetimer-endpoint')
]
