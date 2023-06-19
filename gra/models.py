from django.db import models

# Create your models here.
from django.db import models


from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Ekipy(models.Model):
    nazwa_ekipy = models.CharField(max_length=200, default='')
    sesje_ses_number = models.CharField(max_length=200, default='')
    ekipy_id = models.AutoField(primary_key=True)
    ilosc_punktow = models.IntegerField(default=0)

class Gry(models.Model):
    nr_gry = models.CharField(max_length=200, primary_key=True, default='')
    nazwa_gry = models.CharField(max_length=200, default='')
    czas_trwania = models.CharField(max_length=200, default='')
    lokalizacja = models.CharField(max_length=200, default='')

class Hosty(models.Model):
    h_nick = models.CharField(max_length=200, primary_key=True, default='')
    sesje_ses_number = models.CharField(max_length=200, default='')

class Punktowi(models.Model):
    p_nick = models.CharField(max_length=200, primary_key=True, default='')
    ses_num = models.CharField(max_length=200, default='')
    sesje_ses_number = models.CharField(max_length=200, default='')

class Sesje(models.Model):
    ses_number = models.CharField(max_length=200, default='')
    game_name = models.CharField(max_length=200, default='')
    end_time = models.DateTimeField('end date')
    password = models.CharField(max_length=200, default='')
    gry_nr_gry = models.ForeignKey(Gry, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.ses_number

    def to_delete(self):
        return self.end_time <= timezone.now() - datetime.timedelta(days=7)

class Gracze(models.Model):
    g_nick = models.CharField(max_length = 200, default='')
    score = models.IntegerField(default=0)
    ekipy_ekipy_id = models.ForeignKey(Ekipy, on_delete=models.CASCADE)

    def __str__(self):
        return self.g_nick

class Zadania(models.Model):
    id_zadania = models.CharField(max_length=200, primary_key=True)
    opis_zadania = models.CharField(max_length=200, default='')
    nazwa_zadania = models.CharField(max_length=200, default='')
    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    gry_nr_gry = models.ForeignKey(Gry, on_delete=models.CASCADE)
