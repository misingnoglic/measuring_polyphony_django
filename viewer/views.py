from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from viewer.models import Composition, SourceRelationship, FolioPage
from viewer.logic import mei_to_svg, mei_to_midi, svg_size
from django.http import Http404


def hello(request):
    """
    Renders the home page
    :param request: 
    :return: 
    """
    return render(request, "index.html")


def iiif(request, pk):
    """
    Renders the IIIF link for a piece with a manifest.json link 
    :TODO: Return an error if there's no manifest.json link
    :param request: 
    :param pk: 
    :return: 
    """
    f = Composition.objects.get(pk=pk)
    return render(request, 'iiif.html', context={'url': f.main_source.iiif_manifest})


def svg(request, pk):
    """
    Return the mensural SVG file as an HTTP Response
    :param request: 
    :param pk: 
    :return: 
    """
    piece = Composition.objects.get(pk=pk)
    svg_file = mei_to_svg(piece.mens_mei_file.path)
    return HttpResponse(svg_file, content_type="image/svg+xml")

def cmn_svg(request, pk):
    """
    Return the common SVG file as an HTTP Response
    :param request: 
    :param pk: 
    :return: 
    """
    piece = Composition.objects.get(pk=pk)
    svg_file = mei_to_svg(piece.cmn_mei_file.path, mensural=False)
    return HttpResponse(svg_file, content_type="image/svg+xml")


def midi(request, pk):
    """
    Return the midi as an HTTP response
    :param request: 
    :param pk: 
    :return: 
    """
    piece = Composition.objects.get(pk=pk)
    midi_file = mei_to_midi(piece.cmn_mei_file.path, piece.midi_bpm)
    return HttpResponse(midi_file, content_type="audio/mid")


class CompositionListView(ListView):
    """
    View for listing the compositions - uses build in ListView
    """
    model = Composition

    def get_queryset(self, queryset=None):
        obj = super(CompositionListView, self).get_queryset()
        return obj.filter(is_live=True)


class CompositionDetailView(DetailView):
    """
    View for the composition detail page
    """
    model = Composition

    def get_object(self, queryset=None):
        """
        Overwriting so that we can 404 if it's not live
        :param queryset: 
        :return: 
        """
        obj = super(CompositionDetailView, self).get_object(queryset=queryset)
        if not obj.is_live:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        """
        Adds certain items to the context for rendering the detail page
        :param kwargs: 
        :return: 
        """
        context = super(CompositionDetailView, self).get_context_data(**kwargs)
        folios = FolioPage.objects.filter(source_relationship__composition=self.object, source_relationship__primary=True)
        context['folios'] = folios
        conc_sources = SourceRelationship.objects.filter(composition=self.object, primary=False)
        context['conc_sources'] = conc_sources
        svg = mei_to_svg(Composition.objects.get(pk=self.object.pk).mens_mei_file.path)
        width, height = svg_size(svg)
        context['height'] = height
        context['width'] = width
        return context
