from django.conf.urls import url

from . import views

app_name = 'browse'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.WorkoutDetailView.as_view(), name='workoutdetail'),
    url(r'^celery/$', views.CeleryView, name='celery'),
]
