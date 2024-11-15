from django.db import models

# Create your models here.

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    qr_code = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name