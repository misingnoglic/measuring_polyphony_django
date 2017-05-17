from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^compositions$', views.CompositionListView.as_view(), name='composition-list'),
    url(r'^compositions/(?P<pk>\d+)/$', views.CompositionDetailView.as_view(), name='composition-detail'),
    url(r'^compositions/(?P<pk>\d+)/iiif$', views.iiif, name='composition-iiif'),
]
