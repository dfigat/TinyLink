from django.db import models
from .config import number_of_days, code_length
# Create your models here
#number_of_days jest zmienną przetrzymującą informację ile dni musi minąć bez uzywania linku by tten został usunięty z bazy

class Link(models.Model):
    long_link = models.CharField(max_length=255,unique=True)
    code = models.CharField(max_length=code_length,unique=True)
    lastUsed = models.DateField()