import datetime
from django.utils import timezone
from django.db import models
# Create your models here.


class Poll(models.Model):
    '''Class defines Poll questions table with two columns
    question -> str
    pub_date -> date'''

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    '''Class defines Choices of the Poll questions
    choice_text -> str
    votes -> int'''

    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text