# Generated by Django 4.2.5 on 2023-10-17 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("examination", "0002_chaptergroup_issuedexam_licencecategory_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SelectedQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question",
                    models.TextField(
                        default="", editable=False, verbose_name="Question text"
                    ),
                ),
                (
                    "model_answer",
                    models.TextField(blank=True, verbose_name="Essay model answer"),
                ),
                (
                    "key_points",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        verbose_name="Essay Answer key points",
                    ),
                ),
                (
                    "correct_answer",
                    models.TextField(
                        blank=True, verbose_name="Multichoice correct answer"
                    ),
                ),
                (
                    "alt_answer1",
                    models.TextField(
                        blank=True,
                        verbose_name="Multichoice first wrong alternate answer",
                    ),
                ),
                (
                    "alt_answer2",
                    models.TextField(
                        blank=True,
                        verbose_name="Multichoice second wrong alternatate answer",
                    ),
                ),
                (
                    "alt_answer3",
                    models.TextField(
                        blank=True,
                        verbose_name="Multichoice third wrong alternate answer",
                    ),
                ),
                (
                    "essay_ref",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="examination.essayanswer",
                        verbose_name="The essay question/answer this given answer refers to",
                    ),
                ),
            ],
            options={
                "ordering": ("issued_exam",),
            },
        ),
        migrations.RenameField(
            model_name="chaptergroup",
            old_name="group_name",
            new_name="name",
        ),
        migrations.AlterField(
            model_name="issuedexam",
            name="groupname",
            field=models.ForeignKey(
                max_length=150,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="auth.group",
                verbose_name="The group with the permission to take this exam",
            ),
        ),
        migrations.DeleteModel(
            name="GivenAnswer",
        ),
        migrations.AddField(
            model_name="selectedquestion",
            name="issued_exam",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="examination.issuedexam",
                verbose_name="The examination this given answer belongs to",
            ),
        ),
        migrations.AddField(
            model_name="selectedquestion",
            name="multichoice_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="examination.multichoicequestion",
                verbose_name="The multichoice question this given answer refers to",
            ),
        ),
        migrations.AddConstraint(
            model_name="selectedquestion",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("essay_ref__isnull", True),
                    ("multichoice_ref__isnull", True),
                    _connector="XOR",
                ),
                name="It must refer to an Essay Question exclusive or a Multichoice Question",
            ),
        ),
    ]
