from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings



from . import views

urlpatterns = [
    url(r'^$', views.hello, name='index'),
    url(r'^compositions/?$', views.CompositionListView.as_view(), name='composition-list'),
    url(r'^compositions/(?P<pk>\d+)/$', views.CompositionDetailView.as_view(), name='composition-detail'),
    url(r'^compositions/(?P<pk>\d+)/piece-mens.svg/?$', views.svg_mens, name='composition-svg-mens'),
    url(r'^compositions/(?P<pk>\d+)/piece-cmn.svg/?$', views.svg_cmn, name='composition-svg-cmn'),
    url(r'^compositions/(?P<pk>\d+)/piece.midi/?$', views.midi, name='composition-midi'),
    url(r'^compositions/(?P<pk>\d+)/iiif/?$', views.iiif, name='composition-iiif'),
]+ static("media", document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
