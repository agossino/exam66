# Generated by Django 4.2.5 on 2023-10-01 21:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("examination", "0005_rename_question_id_essayanswer_question_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="essayquestion",
            name="level",
            field=models.IntegerField(choices=[("1", 1), ("2", 2), ("3", 3)]),
        ),
        migrations.AlterField(
            model_name="multichoicequestion",
            name="level",
            field=models.IntegerField(
                choices=[("1", 1), ("2", 2), ("3", 3)], verbose_name="Training level"
            ),
        ),
    ]
