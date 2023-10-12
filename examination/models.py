from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now


class ValidManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(ValidManager, self).get_queryset().filter(valid=True)


LEVEL = ((1, "1"), (2, "2"), (3, "3"))
ANSWER_TYPE = ((1, "Online"), (2, "Printed"))


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
    answer = models.TextField("The right answer")
    alt_answer1 = models.TextField("The first wrong alternate answer")
    alt_answer2 = models.TextField("The second wrong alternatate answer")
    alt_answer3 = models.TextField("The third wrong alternate answer")
    valid = models.BooleanField("Question validity", default=True)
    level = models.IntegerField("Training level", choices=LEVEL)
    saving_time = models.DateTimeField("Saving date", auto_now=True)

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
        return self.text


class EssayQuestion(models.Model):
    objects = models.Manager()
    valid_only = ValidManager()

    module = models.ForeignKey(
        "SubjectModule",
        verbose_name="The module this question belongs to",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    valid = models.BooleanField(default=True)
    level = models.IntegerField(choices=LEVEL)
    saving_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("module", "saving_time")

    def __str__(self) -> str:
        return self.text


class MCQuestionUsage(models.Model):
    usage_date = models.DateField(
        "The date the multichoice question has been used", default=now
    )
    question = models.ForeignKey(MultichoiceQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question {self.question.id} used on {self.usage_date}"


class EssayQuestionUsage(models.Model):
    usage_date = models.DateField(
        "The date the essay question has been used", default=now
    )
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question {self.question.id} used on {self.usage_date}"


class Category(models.Model):
    category = models.CharField("Licence category and subcategory", max_length=5)
    description = models.CharField(max_length=150, default="")

    def __str__(self) -> str:
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class EssayAnswer(models.Model):
    model_answer = models.TextField("Essay model answer")
    key_points = models.CharField("Answer key points", max_length=150)
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return f"Question {self.question.id}; {self.model_answer[:25]}"


class GivenAnswer(models.Model):
    essay_ref = models.ForeignKey(
        EssayAnswer, on_delete=models.SET_NULL, blank=True, null=True
    )
    model_answer = models.TextField("Essay model answer", blank=True)
    key_points = models.CharField("Answer key points", max_length=150, blank=True)

    multichoice_ref = models.ForeignKey(
        MultichoiceQuestion, on_delete=models.SET_NULL, blank=True, null=True
    )
    right_answer = models.TextField("The right answer", blank=True)
    alt_answer1 = models.TextField("The first wrong alternate answer", blank=True)
    alt_answer2 = models.TextField("The second wrong alternatate answer", blank=True)
    alt_answer3 = models.TextField("The third wrong alternate answer", blank=True)

    type = models.IntegerField(choices=ANSWER_TYPE)
    given_answer = models.TextField("The answer given by user")
    assignment_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ("user", "assignment_time")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(essay_ref__isnull=True)
                & ~models.Q(model_answer__exact="")
                & ~models.Q(key_points__exact="")
                | models.Q(essay_ref__isnull=True)
                & models.Q(model_answer__exact="")
                & models.Q(key_points__exact=""),
                name="in essay set: all fields to be filled in or none",
            ),
            models.CheckConstraint(
                check=~models.Q(multichoice_ref__isnull=True)
                & ~models.Q(right_answer__exact="")
                & ~models.Q(alt_answer1__exact="")
                & ~models.Q(alt_answer2__exact="")
                & ~models.Q(alt_answer3__exact="")
                | models.Q(multichoice_ref__isnull=True)
                & models.Q(right_answer__exact="")
                & models.Q(alt_answer1__exact="")
                & models.Q(alt_answer2__exact="")
                & models.Q(alt_answer3__exact=""),
                name="in multichoice set: all fields to be filled in or none",
            ),
            models.CheckConstraint(
                check=~models.Q(essay_ref__isnull=True)
                & ~models.Q(model_answer__exact="")
                & ~models.Q(key_points__exact="")
                ^ ~models.Q(multichoice_ref__isnull=True)
                & ~models.Q(right_answer__exact="")
                & ~models.Q(alt_answer1__exact="")
                & ~models.Q(alt_answer2__exact="")
                & ~models.Q(alt_answer3__exact=""),
                name="fill in only one set between essay multichoice sets",
            ),
        ]

    def __str__(self):
        if self.essay_ref is None:
            question = self.multichoice_ref.text
        else:
            question = self.essay_ref.question.text
        return f"""User: {self.user};
question: {question};
given answer: {self.given_answer}"""


class SubjectModule(models.Model):
    code = models.CharField("Alphanumeric code", max_length=5)
    description = models.CharField(max_length=150)
    category = models.ManyToManyField(Category)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return f"Module {self.code} {self.description}"


class Chapter(models.Model):
    code = models.CharField("Alphanumeric code", max_length=5)
    description = models.CharField(max_length=150)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return f"Module {self.code} {self.description}"
