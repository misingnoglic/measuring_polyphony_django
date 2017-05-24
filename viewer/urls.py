from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings



from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^compositions$', views.CompositionListView.as_view(), name='composition-list'),
    url(r'^compositions/(?P<pk>\d+)/$', views.CompositionDetailView.as_view(), name='composition-detail'),
    url(r'^compositions/(?P<pk>\d+)/iiif$', views.iiif, name='composition-iiif'),
]+ static("media", document_root=settings.MEDIA_ROOT)
