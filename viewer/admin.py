from django.contrib import admin
from .models import Composition, Composer, Genre, Source, Clef, SourceRelationship, Edition, ProjectMember
# Register your models here.


@admin.register(Composition)
class PieceAdmin(admin.ModelAdmin):
    list_display = ['triplum_incipit', 'motetus_incipit', 'tenor_incipit', 'composer', 'main_source', 'edition', 'reference']


@admin.register(Composer, Genre, Source, Clef, SourceRelationship, Edition, ProjectMember)
class GenericAdmin(admin.ModelAdmin):
    pass
