from django.conf.urls import url

import pagetimer.views as views

urlpatterns = [
    url('^$', views.DashboardView.as_view(), name='pagetimer-dashboard'),
    url('^endpoint/$', views.PageTimerEndpointView.as_view(),
        name='pagetimer-endpoint')
]
