from django.db import models
from uuid import uuid4

from .config import number_of_days, code_length
# Create your models here
# number_of_days jest zmienną przetrzymującą informację ile dni musi minąć bez uzywania linku by tten został usunięty z bazy

class Link(models.Model):
    long_link = models.CharField(max_length=255,unique=True)
    code = models.CharField(max_length=code_length,unique=True,default=uuid4)
    lastUsed = models.DateTimeField(auto_now=True)
    
    def get_long_link(self):
        return self.long_link