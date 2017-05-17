from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from viewer.models import Composition, SourceRelationship
from viewer.logic import mei_to_svg



# Create your views here.

def hello(request):
    return render(request, "index.html")

def iiif(request, pk):
    f = Composition.objects.get(pk=pk)
    return render(request, 'iiif.html', context={'url': f.main_source.iiif_manifest})


class CompositionListView(ListView):
    model = Composition


class CompositionDetailView(DetailView):
    model = Composition

    def get_context_data(self, **kwargs):
        context = super(CompositionDetailView, self).get_context_data(**kwargs)
        svg = ""
        if self.object.mens_mei_file:
            svg = mei_to_svg(self.object.mens_mei_file.path)
        context['svg'] = svg
        folios = SourceRelationship.objects.filter(composition=self.object, source=self.object.main_source)
        context['folios'] = folios
        return context
