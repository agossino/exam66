# Generated by Django 4.2.5 on 2023-09-21 16:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("examination", "0004_essayanswer_category_delete_essayanstocategory"),
    ]

    operations = [
        migrations.RenameField(
            model_name="essayanswer",
            old_name="question_id",
            new_name="question",
        ),
        migrations.RenameField(
            model_name="essayquestionusage",
            old_name="question_id",
            new_name="question",
        ),
        migrations.RenameField(
            model_name="mcquestionusage",
            old_name="question_id",
            new_name="question",
        ),
    ]
