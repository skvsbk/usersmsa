from django.db import models

# Create your models here.
class UITUser(models.Model):
        id = models.IntegerField
        name = models.CharField(max_length=50)
        username = models.CharField(max_length=20)
        email = models.CharField(max_length=30)

        street = models.CharField(max_length=30)
        suite = models.CharField(max_length=30)
        city = models.CharField(max_length=20)
        zipcode = models.CharField(max_length=10)

        lat = models.FloatField()
        lng = models.FloatField()

        phone = models.CharField(max_length=25)
        website = models.CharField(max_length=20)

        company_name = models.CharField(max_length=30)
        catchPhrase = models.CharField(max_length=100)
        bs = models.CharField(max_length=100)

        def __str__(self):
            return self.name