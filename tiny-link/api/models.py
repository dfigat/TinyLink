from django.db import models
from random import choices
from string import ascii_letters, digits

from .config import number_of_days, code_length
# Create your models here
# number_of_days jest zmienną przetrzymującą informację ile dni musi minąć bez uzywania linku by tten został usunięty z bazy

def get_code(code_length=code_length):
    def generate_code(code_length):
        return ''.join(choices(ascii_letters + digits, k=code_length))
    
    # Make sure there are no duplicates
    code =  generate_code(code_length)
    while Link.objects.filter(code = code):
        code = generate_code(code_length)
    
    return code

class Link(models.Model):
    long_link = models.URLField(max_length=255,unique=True)
    code = models.CharField(max_length=code_length,unique=True,default=get_code)
    lastUsed = models.DateTimeField(auto_now=True)
    
    def get_long_link(self):
        return self.long_link