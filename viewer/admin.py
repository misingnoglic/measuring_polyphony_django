from django.contrib import admin
from .models import Composition, Composer, Genre, Source, Clef, SourceRelationship, Edition, ProjectMember, FolioPage
# Register your models here.


class SourceRelationshipInline(admin.TabularInline):
    model = SourceRelationship


class FolioPageInline(admin.TabularInline):
    model = FolioPage

@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ['triplum_incipit', 'motetus_incipit', 'tenor_incipit', 'composer', 'main_source', 'edition', 'reference']
    inlines = [SourceRelationshipInline]


@admin.register(SourceRelationship)
class SourceRelationshipAdmin(admin.ModelAdmin):
    inlines = [FolioPageInline]


@admin.register(Composer, Genre, Source, Clef, Edition, ProjectMember, FolioPage)
class GenericAdmin(admin.ModelAdmin):
    pass
