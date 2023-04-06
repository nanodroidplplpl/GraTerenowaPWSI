from django.db import models

# Create your models here.
from django.db import models


from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Sesje(models.Model):
    ses_number = models.CharField(max_length=200)
    game_name = models.CharField(max_length=200)
    end_time = models.DateTimeField('end date')
    password = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.ses_number

    def to_delete(self):
        return self.end_time <= timezone.now() - datetime.timedelta(days=7)

class Gracze(models.Model):
    ses = models.ForeignKey(Sesje, on_delete=models.CASCADE)
    g_nick = models.CharField(max_length = 200)
    score = models.IntegerField()

    def __str__(self):
        return self.g_nick