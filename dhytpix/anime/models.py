from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


ANIME_CATEGORIES = (
    ('ACAO', 'Ação'),
    ('AVENTURA', 'Aventura'),
    ('DRAMA', 'Drama'),
    ('COMÉDIA', 'Comédia'),
    ('ROMANCE', 'Romance'),
    ('SCI-FI', 'Sci-Fi'),
    ('TERROR', 'Terror'),
    ('MISTERIO', 'Mistério'),
    ('SHONEN', 'Shōnen'),
    ('SHOUNEN', 'Shounen'),
    ('SEINEN', 'Seinen'),
    ('SHOJO', 'Shōjo'),
    ('JOSEI', 'Josei'),
    ('KODOMO', 'Kodomo'),
    ('UNDEFINED', 'Indefinido'),
    ('SEINEN/TERROR', 'Seinen/Terror'),
    ('MYSTERY/TERROR', 'Mistério/Terror'),
)


# modelo de exibição de episódio;
class Anime(models.Model):
    name = models.CharField(max_length=1000)
    thumb = models.ImageField(upload_to='thumbs')
    description = models.TextField(max_length=10000)
    link = models.URLField()
    category = models.CharField(max_length=1000, choices=ANIME_CATEGORIES)
    views = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class User(AbstractUser):
    historic_animes = models.ManyToManyField("Anime")
