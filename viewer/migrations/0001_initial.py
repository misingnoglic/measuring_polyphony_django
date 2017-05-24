# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 16:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.CharField(max_length=1)),
                ('number', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('letter', 'number'),
            },
        ),
        migrations.CreateModel(
            name='Composer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_live', models.BooleanField(default=True)),
                ('triplum_incipit', models.CharField(max_length=200)),
                ('motetus_incipit', models.CharField(max_length=200)),
                ('tenor_incipit', models.CharField(blank=True, max_length=200)),
                ('contratenor_incipit', models.CharField(blank=True, max_length=200)),
                ('quadruplum_incipit', models.CharField(blank=True, max_length=200)),
                ('short_title', models.CharField(blank=True, max_length=200, null=True)),
                ('attributed_composer', models.BooleanField(default=True)),
                ('number_voices', models.IntegerField()),
                ('modus', models.CharField(blank=True, max_length=10, null=True)),
                ('tempus', models.CharField(blank=True, max_length=10, null=True)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('cmn_mei_file', models.FileField(upload_to='common_mei/')),
                ('mens_mei_file', models.FileField(upload_to='mensural_mei/')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='pdf/')),
                ('mp3_file', models.FileField(blank=True, null=True, upload_to='mp3/')),
                ('diamm_composition_id', models.CharField(max_length=200)),
                ('transcription_entered', models.DateField(blank=True, null=True)),
                ('mens_mei_created', models.DateField(blank=True, null=True)),
                ('transcription_comments', models.CharField(blank=True, max_length=500)),
                ('notes_on_motet_texts', models.CharField(blank=True, max_length=500)),
                ('variants_description', models.CharField(blank=True, max_length=2000)),
                ('additional_comments_on_database_record', models.CharField(blank=True, max_length=500)),
                ('clefs', models.ManyToManyField(to='viewer.Clef')),
                ('composer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.Composer')),
            ],
            options={
                'ordering': ('triplum_incipit', 'motetus_incipit'),
            },
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('author',),
            },
        ),
        migrations.CreateModel(
            name='FolioPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio_number', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('order_number', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('source_relationship', '-folio_number'),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initials', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('initials',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('signal', models.CharField(max_length=10)),
                ('iiif_manifest', models.URLField(blank=True, null=True)),
                ('diamm_source', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SourceRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.BooleanField(default=False)),
                ('text_only', models.BooleanField(default=False)),
                ('diamm_item_id', models.IntegerField(blank=True, null=True)),
                ('composition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.Composition')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.Source')),
            ],
            options={
                'ordering': ('source', 'composition'),
            },
        ),
        migrations.AddField(
            model_name='foliopage',
            name='source_relationship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.SourceRelationship'),
        ),
        migrations.AddField(
            model_name='composition',
            name='edition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.Edition'),
        ),
        migrations.AddField(
            model_name='composition',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.Genre'),
        ),
        migrations.AddField(
            model_name='composition',
            name='main_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.Source'),
        ),
        migrations.AddField(
            model_name='composition',
            name='mens_mei_creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mei_creator', to='viewer.ProjectMember'),
        ),
        migrations.AddField(
            model_name='composition',
            name='transcriber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transcriber', to='viewer.ProjectMember'),
        ),
        migrations.AddField(
            model_name='composition',
            name='transcription_checked_by',
            field=models.ManyToManyField(related_name='transcriber_checker', to='viewer.ProjectMember'),
        ),
    ]
