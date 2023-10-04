from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.timezone import now


class ValidManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(ValidManager, self).get_queryset().filter(valid=True)


LEVEL = ((1, "1"), (2, "2"), (3, "3"))


class MultichoiceQuestion(models.Model):
    objects = models.Manager()
    valid_only = ValidManager()

    text = models.TextField("Question text")
    module = models.CharField(
        "The module this question belongs to", max_length=5, blank=True
    )
    chapter = models.CharField(
        "The chapter this question belongs to", max_length=5, blank=True
    )
    answer = models.TextField("The right answer")
    alt_answer1 = models.TextField("The first wrong alternate answer")
    alt_answer2 = models.TextField("The second wrong alternatate answer")
    alt_answer3 = models.TextField("The third wrong alternate answer")
    valid = models.BooleanField("Question validity", default=True)
    level = models.IntegerField("Training level", choices=LEVEL)
    saving_date = models.DateField("Saving date", auto_now=True)

    def get_absolute_url(self):
        return reverse("detail_mcquest", args=[self.id])

    class Meta:
        ordering = ("-saving_date", "module", "chapter")

    def __str__(self) -> str:
        return self.text


class EssayQuestion(models.Model):
    objects = models.Manager()
    valid_only = ValidManager()

    module = models.CharField(max_length=5)
    text = models.TextField()
    valid = models.BooleanField(default=True)
    level = models.IntegerField(choices=LEVEL)
    saving_date = models.DateField(auto_now=True)

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

    def __str__(self) -> str:
        return self.category


class EssayAnswer(models.Model):
    answer = models.TextField("Essay answer")
    key_points = models.CharField("Answer key points", max_length=150)
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return f"Question {self.question.id}; {self.answer[:25]}"
