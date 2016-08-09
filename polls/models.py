from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """

        :return: str
        """
        return self.question_text

    def was_published_recently(self):
        """
        Predicate to see if a question was created recently in the past.
        :return: bool
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    #admin options
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #this allows Question instances to access Choice that associate to it through choice_set and member functions like choice_set.all() 
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """

        :return: str
        """
        return self.choice_text
