from django.db import models

# Create your models here.


class Composer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=100)
    signal = models.CharField(max_length=10)
    iiif_manifest = models.URLField(blank=True, null=True)
    diamm_source = models.URLField(blank=True, null=True)
    diamm_source = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Clef(models.Model):
    letter = models.CharField(max_length=1)
    number = models.PositiveSmallIntegerField()
    def __str__(self):
        return "{}{}".format(self.letter, self.number)


class SourceRelationship(models.Model):
    source = models.ForeignKey(Source)
    folio_number = models.CharField(max_length=20, null=True, blank=True)
    composition = models.ForeignKey("Composition")
    primary = models.BooleanField(default=False)
    text_only = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    diamm_item_id = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return "{} - Folio #{}".format(self.source.name, self.folio_number)


class Edition(models.Model):
    author = models.CharField(max_length=20)
    def __str__(self):
        return self.author

class ProjectMember(models.Model):
    initials = models.CharField(max_length=5)
    name = models.CharField(max_length=20)
    def __str__(self):
        return "{}".format(self.initials)

class Composition(models.Model):
    triplum_incipit = models.CharField(max_length=200)
    motetus_incipit = models.CharField(max_length=200)
    tenor_incipit = models.CharField(max_length=200, blank=True)
    contratenor_incipit = models.CharField(max_length=200, blank=True)
    quadruplum_incipit = models.CharField(max_length=200, blank=True)
    short_title = models.CharField(max_length=200, null=True, blank=True)
    composer = models.ForeignKey(Composer)
    attributed_composer = models.BooleanField(default=True)
    genre = models.ForeignKey(Genre)
    main_source = models.ForeignKey(Source)
    number_voices = models.IntegerField()
    clefs = models.ManyToManyField(Clef)
    modus = models.CharField(null=True, blank=True, max_length=10)
    tempus = models.CharField(null=True, blank=True, max_length=10)
    edition = models.ForeignKey(Edition, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    cmn_mei_file = models.FileField(upload_to="common_mei/")
    mens_mei_file = models.FileField(upload_to="mensural_mei/")
    pdf_file = models.FileField(upload_to="pdf/", null=True, blank=True)
    mp3_file = models.FileField(upload_to="mp3/", null=True, blank=True)
    diamm_composition_id = models.CharField(max_length=200)
    transcriber = models.ForeignKey(ProjectMember, related_name="transcriber", null=True, blank=True)
    transcription_entered = models.DateField(null=True, blank=True)
    transcription_checked_by = models.ManyToManyField(ProjectMember, "transcriber_checker")
    mens_mei_creator = models.ForeignKey(ProjectMember, related_name="mei_creator", null=True, blank=True)
    mens_mei_created = models.DateField(null=True, blank=True)
    transcription_comments = models.CharField(max_length=500, blank=True)
    notes_on_motet_texts = models.CharField(max_length=500, blank=True)
    variants_description = models.CharField(max_length=2000, blank=True)
    additional_comments_on_database_record = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.triplum_incipit}/{self.motetus_incipit}"


