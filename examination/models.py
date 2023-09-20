from django.db import models

class MultiChoiceQuestion(models.Model):
    text = models.TextField("Question text")
    module = models.CharField("The module this question belongs to", max_length=5)
    chapter = models.CharField("The chapter this question belongs to", max_length=5)
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
    mudule = models.CharField(max_length=5)
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
    usage_data = models.DateField()
    question_id = models.ForeignKey(MultiChoiceQuestion, on_delete=models.CASCADE)


class EssayQuestionUsage(models.Model):
    usage_data = models.DateField()
    question_id = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)

class EssayAnswer(models.Model):
    answer = models.TextField("Essay answer")
    key_points = models.CharField("Answer key points", max_length=150)
    question_id = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)

class Category(models.Model):
    category = models.CharField("Licence category and subcategory", max_length=5)

class EssayAnsToCategory(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(EssayAnswer, on_delete=models.CASCADE)