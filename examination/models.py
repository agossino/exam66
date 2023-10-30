from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import Group, User
from django.urls import reverse


class ValidManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(ValidManager, self).get_queryset().filter(is_valid=True)


LEVEL = ((1, "1"), (2, "2"), (3, "3"))
EXAMINATION_TYPE = ((1, "Online"), (2, "Printout"))


class MultichoiceQuestion(models.Model):
    objects = models.Manager()
    valid_only = ValidManager()

    text = models.TextField("Question text")
    module = models.ForeignKey(
        "SubjectModule",
        verbose_name="The module this question belongs to",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    chapter = models.ForeignKey(
        "Chapter",
        verbose_name="The chapter this question belongs to",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    answer = models.TextField("The correct answer")
    alt_answer1 = models.TextField("The first wrong alternate answer")
    alt_answer2 = models.TextField("The second wrong alternatate answer")
    # TODO alt_answer3 to be deleted
    alt_answer3 = models.TextField("The third wrong alternate answer")
    is_valid = models.BooleanField("Question validity", default=True)
    level = models.IntegerField("Training level", choices=LEVEL)
    saving_time = models.DateTimeField("Saving time", auto_now=True)

    def get_absolute_url(self):
        return reverse("detail_mcquest", args=[self.id])

    class Meta:
        ordering = ("module", "chapter", "saving_time")
        constraints = [
            models.CheckConstraint(
                check=models.Q(module__isnull=True) ^ models.Q(chapter__isnull=True),
                name="module_xor_chapter",
            )
        ]

    def __str__(self) -> str:
        return f"Multichoice Question: {self.text}"


class EssayQuestion(models.Model):
    objects = models.Manager()
    valid_only = ValidManager()

    module = models.ForeignKey(
        "SubjectModule",
        verbose_name="The module this question belongs to",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    text = models.TextField("Question text")
    is_valid = models.BooleanField("Question validity", default=True)
    level = models.IntegerField("Training level", choices=LEVEL)
    saving_time = models.DateTimeField("Saving time", auto_now=True)

    class Meta:
        ordering = ("module", "saving_time")

    def __str__(self) -> str:
        return f"Essay Question: {self.text}"


# TODO code = models.CharField("Licence category and subcategory code", unique=True, max_length=5)
class LicenceCategory(models.Model):
    code = models.CharField("Licence category and subcategory code", max_length=5)
    description = models.CharField(max_length=150, default="")

    def __str__(self) -> str:
        return f"Licence Category: {self.code}"

    class Meta:
        verbose_name_plural = "LicenceCategories"


class EssayAnswer(models.Model):
    model_answer = models.TextField("Essay model answer")
    key_points = models.CharField("Answer key points", max_length=150)
    question = models.ForeignKey(
        EssayQuestion,
        verbose_name="The answer this question responds to",
        on_delete=models.CASCADE,
    )
    licence_category = models.ManyToManyField(
        LicenceCategory,
        verbose_name="Licence category and subcategory this question belongs to",
    )

    def __str__(self) -> str:
        return f"Answer: {self.model_answer}; to Question Essay: {self.question.id}"


class IssuedExam(models.Model):
    creation_time = models.DateTimeField("Creation time", auto_now_add=True)
    handout_time = models.DateTimeField("The time exam is handed out", null=True)
    # TODO
    # exam_tag = models.CharField(
    #     "The name used to uniquely identify the examination", unique=True
    # )
    exam_identifier = models.CharField(
        "The name used to uniquely identify the examination", unique=True
    )
    type = models.IntegerField(
        "The way this examination is given", choices=EXAMINATION_TYPE, null=True
    )
    groupname = models.ForeignKey(
        Group,
        verbose_name="The group with the permission to take this exam",
        on_delete=models.SET_NULL,
        null=True,
        max_length=150,
    )

    def __str__(self) -> str:
        return f"Issued Exam: {self.exam_identifier}"


class SelectedQuestion(models.Model):
    question = models.TextField("Question text", editable=False, default="")

    # This instance can refers to an essay question/answer, exclusive or ...
    essay_ref = models.ForeignKey(
        EssayAnswer,
        verbose_name="The essay question/answer this given answer refers to",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    model_answer = models.TextField("Essay model answer", blank=True)
    key_points = models.CharField("Essay Answer key points", max_length=150, blank=True)
    # ... can refers to a multichoice question
    multichoice_ref = models.ForeignKey(
        MultichoiceQuestion,
        verbose_name="The multichoice question this given answer refers to",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    correct_answer = models.TextField("Multichoice correct answer", blank=True)
    alt_answer1 = models.TextField(
        "Multichoice first wrong alternate answer", blank=True
    )
    alt_answer2 = models.TextField(
        "Multichoice second wrong alternatate answer", blank=True
    )
    # TODO alt_answer3 to be deleted
    alt_answer3 = models.TextField(
        "Multichoice third wrong alternate answer", blank=True
    )

    issued_exam = models.ForeignKey(
        IssuedExam,
        verbose_name="The examination this given answer belongs to",
        on_delete=models.PROTECT,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.essay_ref is None:
            self.question = self.multichoice_ref.text
            self.correct_answer = self.multichoice_ref.answer
            self.alt_answer1 = self.multichoice_ref.alt_answer1
            self.alt_answer2 = self.multichoice_ref.alt_answer2
            self.alt_answer3 = self.multichoice_ref.alt_answer3
        else:
            self.question = self.essay_ref.question.text
            self.model_answer = self.essay_ref.model_answer
            self.key_points = self.essay_ref.key_points
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("issued_exam",)
        # TODO
        # constraints = [
        #     models.CheckConstraint(
        #         check=models.Q(essay_ref__isnull=True)
        #         ^ models.Q(multichoice_ref__isnull=True),
        #         name="Refer to an Essay Question xor a Multichoice Question",
        #     ),
        # ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(essay_ref__isnull=True)
                ^ models.Q(multichoice_ref__isnull=True),
                name="It must refer to an Essay Question exclusive or a Multichoice Question",
            ),
        ]

    def __str__(self):
        return f"Selected Question: {self.question}"


class GivenAnswer(models.Model):
    answer = models.TextField("The answer given by the examinee", blank=True)
    is_correct = models.BooleanField("Is the given answer correct?", null=True)
    saving_time = models.DateTimeField("Saving time", auto_now=True)
    creation_time = models.DateTimeField("Creation time", auto_now_add=True)
    question = models.ForeignKey(
        SelectedQuestion,
        verbose_name="The question this answer respond to",
        on_delete=models.PROTECT,
    )
    username = models.ForeignKey(
        User,
        verbose_name="Examinee who takes the exam",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        permissions = [
            ("change_givenanswer_is_correct", "Can change given answer is_correct"),
            ("view_givenanswer_is_correct", "Can view given answer is_correct"),
        ]

    def __str__(self):
        return f"Given Answer: {self.answer} on {self.saving_time} by {self.username}"


class SubjectModule(models.Model):
    code = models.CharField("Subject Module alphanumeric code", max_length=5)
    description = models.CharField("Subject Module description", max_length=150)
    licence_category = models.ManyToManyField(
        LicenceCategory,
        verbose_name="Licence category and subcategory this module refers to",
    )

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return f"Subject Module: {self.code} {self.description}"


class ChapterGroup(models.Model):
    name = models.CharField(
        "The name of the group, which consists of many Chapters", max_length=300
    )

    def __str__(self) -> str:
        return f"Chapter Group: {self.name}"


class Chapter(models.Model):
    code = models.CharField("Chapter alphanumeric code", max_length=5)
    description = models.CharField("Chapter description", max_length=300)
    group_name = models.ForeignKey(
        ChapterGroup,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="The name of the group, which consists of many Chapters",
    )

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return f"Chapter: {self.code} {self.description}"
