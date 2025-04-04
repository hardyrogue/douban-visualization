from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    cover = models.URLField(blank=True)

    def __str__(self):
        return self.title
