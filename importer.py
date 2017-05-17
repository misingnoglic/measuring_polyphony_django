import csv
import datetime
from django.core.exceptions import ObjectDoesNotExist
from measuring_polyphony.settings import BASE_DIR
import progressbar

import os
os.system("del db.sqlite3")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "measuring_polyphony.settings")
import django
django.setup()

from viewer.models import *



from django.conf import settings
bar = progressbar.ProgressBar(max_value=64)

ss = csv.DictReader(open('measuring.csv', encoding='utf8'))
for line in bar(ss):
    np = Composition()
    titles = line['Title'].split("/")
    np.triplum_incipit=titles[0].strip()
    if len(titles)>1:
        np.motetus_incipit = titles[1].strip()
    if len(titles)>2:
        np.tenor_incipit = titles[2].strip()

    comp_name = line['Composer']
    try:
        comp = Composer.objects.get(name=comp_name)
    except ObjectDoesNotExist:
        comp = Composer(name=comp_name)
        comp.save()

    np.composer = comp

    att = line["Attrib"]
    if att=="TRUE":
        np.attributed_composer = True
    else:
        np.attributed_composer = False

    genre_name = line['Genre']
    try:
        genre = Genre.objects.get(name=genre_name)
    except ObjectDoesNotExist:
        genre = Genre(name=genre_name)
        genre.save()

    np.genre = genre

    man_source_name = line["Manuscript_source"]
    try:
        main_source = Source.objects.get(name=man_source_name)
    except ObjectDoesNotExist:
        main_source = Source(name=man_source_name)
        main_source.iiif_manifest = line["IIIF_manifest"]
        main_source.diamm_source = line["DIAMM_source"]
        main_source.online_image = line["Other_online_images"]
        main_source.save()

    np.main_source = main_source
    np.number_voices = int(line["Number_of_voices"])


    if line["Modus"]:
        np.modus = line["Modus"]

    if line["Tempus"]:
        np.tempus = line["Tempus"]

    if line["Primary Edition"]:
        try:
            ed = Edition.objects.get(author=line["Primary Edition"])
        except ObjectDoesNotExist:
            ed = Edition(author=line["Primary Edition"])
            ed.save()
        np.edition = ed

    np.reference = line['Reference']
    if line["MEI_CMN_file"]:
        l = line["MEI_CMN_file"].replace("/", "\\").split("\\")
        cmnmei_dir =  os.path.join(BASE_DIR, "mei_files", *l)
        np.cmn_mei_file.save(l[-1], open(cmnmei_dir))

    if line["MEI_MENS_file"]:
        l = line["MEI_MENS_file"].replace("/", "\\").split("\\")
        menmei_dir = os.path.join(BASE_DIR, "mei_files", *l)
        np.mens_mei_file.save(l[-1], open(menmei_dir))



    try:
        transcriber = ProjectMember.objects.get(initials=line["Transcription_entered_by"])
    except ObjectDoesNotExist:
        transcriber = ProjectMember(initials=line["Transcription_entered_by"])
        transcriber.save()
    np.transcriber = transcriber
    if line["Transcription_entered_date"]:
        np.transcription_entered = datetime.datetime.strptime(line["Transcription_entered_date"], "%m/%d/%Y").date()




    try:
        transcriber = ProjectMember.objects.get(initials=line["MEI_MENS_created_by"])
    except ObjectDoesNotExist:
        transcriber = ProjectMember(initials=line["MEI_MENS_created_by"])
        transcriber.save()
    np.mens_mei_creator = transcriber
    if line["MEI_MENS_created_date"]:
        try:
            np.mens_mei_created = datetime.datetime.strptime(line["MEI_MENS_created_date"], "%m/%d/%Y").date()
        except ValueError:
            np.mens_mei_created = datetime.datetime.strptime(line["MEI_MENS_created_date"], "%m/%d/%y").date()


    np.transcription_comments = line["Additional_comments_on_transcription"]
    np.notes_on_motet_texts = line["Notes_on_motet_texts"]

    np.variants_description = line["Variants_description"]
    np.additional_comments_on_database_record = line["Additional_comments_on_database_record"]
    np.save()





    # after np is saved

    clefs = line["Clefs"].split(',')
    for source_name in clefs:
        if source_name:
            c2 = source_name.strip()
            l = c2[0]
            n = int(c2[1])
            try:
                clef = Clef.objects.get(letter=l, number=n)
            except ObjectDoesNotExist:
                clef = Clef(letter=l, number=n)
                clef.save()
            np.clefs.add(clef)

    checked = line["Transcription_checked_by"].split(", ")
    for c in checked:
        try:
            transcriber = ProjectMember.objects.get(initials=c)
        except ObjectDoesNotExist:
            transcriber = ProjectMember(initials=c)
            transcriber.save()

        np.transcription_checked_by.add(transcriber)

    np.save()

    folio_nums = line["Folio_numbers"].split(",")
    for n in folio_nums:
        sr = SourceRelationship(source=main_source, folio_number=n.strip(), composition = np, primary=True)
        sr.save()

    conc_sources = line["Concordant_Sources"].split(",")
    for conc in conc_sources:
        source_name = conc.strip()
        if source_name:
            words = source_name.split()
            text_only = False
            if words[-1].lower() == "(text)":
                text_only = True
                source_name = " ".join(words[:-1])
            elif words[-1].lower() == "(index)":
                source_name = " ".join(words[:-1])

            try:
                source = Source.objects.get(name=source_name)
            except ObjectDoesNotExist:
                source = Source(name=source_name)
                source.save()

            cs = SourceRelationship(source=source, composition=np, primary=False,
                                text_only=text_only)

            cs.save()

os.system("python manage.py createsuperuser")



