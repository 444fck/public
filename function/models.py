from django.db import models

class Configuration(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    config = models.IntegerField()
    source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class FeedBack(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name} {self.feedback}"
