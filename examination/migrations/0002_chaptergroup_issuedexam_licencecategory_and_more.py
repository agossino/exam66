# Generated by Django 4.2.5 on 2023-10-16 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("examination", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChapterGroup",
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
                    "group_name",
                    models.CharField(
                        max_length=300,
                        verbose_name="The name of the group, which consists of many Chapters",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IssuedExam",
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
                    "creation_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation datetime"
                    ),
                ),
                (
                    "handout_time",
                    models.DateTimeField(
                        null=True, verbose_name="The datetime exam is handed out"
                    ),
                ),
                (
                    "exam_identifier",
                    models.CharField(
                        unique=True,
                        verbose_name="The name used to uniquely identify the examination",
                    ),
                ),
                (
                    "type",
                    models.IntegerField(
                        choices=[(1, "Online"), (2, "Printout")],
                        null=True,
                        verbose_name="The way this examination is given",
                    ),
                ),
                (
                    "groupname",
                    models.CharField(
                        max_length=150,
                        verbose_name="The group with the permission to take this exam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LicenceCategory",
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
                    "code",
                    models.CharField(
                        max_length=5,
                        verbose_name="Licence category and subcategory code",
                    ),
                ),
                ("description", models.CharField(default="", max_length=150)),
            ],
            options={
                "verbose_name_plural": "LicenceCategories",
            },
        ),
        migrations.RemoveField(
            model_name="essayquestionusage",
            name="question",
        ),
        migrations.RemoveField(
            model_name="mcquestionusage",
            name="question",
        ),
        migrations.AlterModelOptions(
            name="givenanswer",
            options={"ordering": ("username", "assignment_time")},
        ),
        migrations.RemoveConstraint(
            model_name="givenanswer",
            name="in essay set: all fields to be filled in or none",
        ),
        migrations.RemoveConstraint(
            model_name="givenanswer",
            name="in multichoice set: all fields to be filled in or none",
        ),
        migrations.RemoveConstraint(
            model_name="givenanswer",
            name="fill in only one set between essay multichoice sets",
        ),
        migrations.RenameField(
            model_name="multichoicequestion",
            old_name="valid",
            new_name="is_valid",
        ),
        migrations.RemoveField(
            model_name="essayanswer",
            name="category",
        ),
        migrations.RemoveField(
            model_name="essayquestion",
            name="valid",
        ),
        migrations.RemoveField(
            model_name="givenanswer",
            name="right_answer",
        ),
        migrations.RemoveField(
            model_name="givenanswer",
            name="type",
        ),
        migrations.RemoveField(
            model_name="givenanswer",
            name="user",
        ),
        migrations.RemoveField(
            model_name="subjectmodule",
            name="category",
        ),
        migrations.AddField(
            model_name="essayquestion",
            name="is_valid",
            field=models.BooleanField(default=True, verbose_name="Question validity"),
        ),
        migrations.AddField(
            model_name="givenanswer",
            name="correct_answer",
            field=models.TextField(
                blank=True, verbose_name="Multichoice correct answer"
            ),
        ),
        migrations.AddField(
            model_name="givenanswer",
            name="is_correct",
            field=models.BooleanField(
                null=True, verbose_name="Is the given answer correct?"
            ),
        ),
        migrations.AddField(
            model_name="givenanswer",
            name="question",
            field=models.TextField(
                default="", editable=False, verbose_name="Question text"
            ),
        ),
        migrations.AddField(
            model_name="givenanswer",
            name="username",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Examinee who takes the exam",
            ),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="code",
            field=models.CharField(
                max_length=5, verbose_name="Chapter alphanumeric code"
            ),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="description",
            field=models.CharField(max_length=300, verbose_name="Chapter description"),
        ),
        migrations.AlterField(
            model_name="essayanswer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="examination.essayquestion",
                verbose_name="The answer this question responds to",
            ),
        ),
        migrations.AlterField(
            model_name="essayquestion",
            name="level",
            field=models.IntegerField(
                choices=[(1, "1"), (2, "2"), (3, "3")], verbose_name="Training level"
            ),
        ),
        migrations.AlterField(
            model_name="essayquestion",
            name="module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="examination.subjectmodule",
                verbose_name="The module this question belongs to",
            ),
        ),
        migrations.AlterField(
            model_name="essayquestion",
            name="saving_time",
            field=models.DateTimeField(auto_now=True, verbose_name="Saving date"),
        ),
        migrations.AlterField(
            model_name="essayquestion",
            name="text",
            field=models.TextField(verbose_name="Question text"),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="alt_answer1",
            field=models.TextField(
                blank=True, verbose_name="Multichoice first wrong alternate answer"
            ),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="alt_answer2",
            field=models.TextField(
                blank=True, verbose_name="Multichoice second wrong alternatate answer"
            ),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="alt_answer3",
            field=models.TextField(
                blank=True, verbose_name="Multichoice third wrong alternate answer"
            ),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="assignment_time",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="The time this answer is given"
            ),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="essay_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="examination.essayanswer",
                verbose_name="The essay question/answer this given answer refers to",
            ),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="given_answer",
            field=models.TextField(verbose_name="The answer given by the examinee"),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="key_points",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="Essay Answer key points"
            ),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="model_answer",
            field=models.TextField(blank=True, verbose_name="Essay model answer"),
        ),
        migrations.AlterField(
            model_name="givenanswer",
            name="multichoice_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="examination.multichoicequestion",
                verbose_name="The multichoice question this given answer refers to",
            ),
        ),
        migrations.AlterField(
            model_name="multichoicequestion",
            name="answer",
            field=models.TextField(verbose_name="The correct answer"),
        ),
        migrations.AlterField(
            model_name="subjectmodule",
            name="code",
            field=models.CharField(
                max_length=5, verbose_name="Subject Module alphanumeric code"
            ),
        ),
        migrations.AlterField(
            model_name="subjectmodule",
            name="description",
            field=models.CharField(
                max_length=150, verbose_name="Subject Module description"
            ),
        ),
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.DeleteModel(
            name="EssayQuestionUsage",
        ),
        migrations.DeleteModel(
            name="MCQuestionUsage",
        ),
        migrations.AddField(
            model_name="chapter",
            name="group_name",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="examination.chaptergroup",
                verbose_name="The name of the group, which consists of many Chapters",
            ),
        ),
        migrations.AddField(
            model_name="essayanswer",
            name="licence_category",
            field=models.ManyToManyField(
                to="examination.licencecategory",
                verbose_name="Licence category and subcategory this question belongs to",
            ),
        ),
        migrations.AddField(
            model_name="givenanswer",
            name="issued_exam",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="examination.issuedexam",
                verbose_name="The examination this given answer belongs to",
            ),
        ),
        migrations.AddField(
            model_name="subjectmodule",
            name="licence_category",
            field=models.ManyToManyField(
                to="examination.licencecategory",
                verbose_name="Licence category and subcategory this module refers to",
            ),
        ),
    ]
