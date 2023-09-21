from django.db import models
from django.utils.timezone import now


class MultichoiceQuestion(models.Model):
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
    valid = models.BooleanField("Questio validity", default=True)

    class Level(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3

    level = models.IntegerField("Training level", choices=Level.choices)
    saving_date = models.DateField("Saving date", auto_now=True)

    def __str__(self) -> str:
        return self.text


class EssayQuestion(models.Model):
    module = models.CharField(max_length=5)
    text = models.TextField()
    valid = models.BooleanField(default=True)

    class Level(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3

    level = models.IntegerField(choices=Level.choices)
    saving_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.text


class MCQuestionUsage(models.Model):
    usage_date = models.DateField(
        "The date the multichoice question has been used", default=now
    )
    question = models.ForeignKey(MultichoiceQuestion, on_delete=models.CASCADE)


class EssayQuestionUsage(models.Model):
    usage_date = models.DateField(
        "The date the essay question has been used", default=now
    )
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)


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
        return str(self.question)
