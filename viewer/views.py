from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from viewer.models import Composition, SourceRelationship, FolioPage
from viewer.logic import mei_to_svg, mei_to_midi



# Create your views here.

def hello(request):
    return render(request, "index.html")


def iiif(request, pk):
    f = Composition.objects.get(pk=pk)
    return render(request, 'iiif.html', context={'url': f.main_source.iiif_manifest})


def svg_mens(request, pk):
    piece = Composition.objects.get(pk=pk)
    svg_file = mei_to_svg(piece.mens_mei_file.path)
    return HttpResponse(svg_file, content_type="image/svg+xml")

def svg_cmn(request, pk):
    piece = Composition.objects.get(pk=pk)
    svg_file = mei_to_svg(piece.cmn_mei_file.path, mensural=False)
    return HttpResponse(svg_file, content_type="image/svg+xml")


def midi(request, pk):
    piece = Composition.objects.get(pk=pk)
    midi_file = mei_to_midi(piece.cmn_mei_file.path)
    return HttpResponse(midi_file, content_type="audio/mid")


class CompositionListView(ListView):
    model = Composition


class CompositionDetailView(DetailView):
    model = Composition

    def get_context_data(self, **kwargs):
        context = super(CompositionDetailView, self).get_context_data(**kwargs)
        svg = ""
        folios = FolioPage.objects.filter(source_relationship__composition=self.object, source_relationship__primary=True)
        context['folios'] = folios
        conc_sources = SourceRelationship.objects.filter(composition=self.object, primary=False)
        context['conc_sources'] = conc_sources
        return context
