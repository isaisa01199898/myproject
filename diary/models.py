from django.db import models

class Diary(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    diary_date = models.DateField()

    def __str__(self):
        return self.title
