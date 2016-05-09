from django.conf.urls import url

import pagetimer.views as views

urlpatterns = [
    url('^endpoint/$', views.PageTimerEndpointView.as_view(),
        name='pagetimer-endpoint')
]
