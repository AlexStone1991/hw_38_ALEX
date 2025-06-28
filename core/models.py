from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
