import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(blank=False, upload_to="images/avatar", verbose_name="avatar")


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = models.TextField(max_length=5000)
    summary_content = models.TextField(max_length=1000)
    image = models.ImageField(blank=True, upload_to="images/avatar")
    question_votes = models.IntegerField(default=0)

    @property
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def procent(self):
        return 100 * self.votes / self.question.question_votes


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
