from django.db import models
import uuid
from auth_user.models import *
from datetime import datetime

category_choices = [
    ('Ação', 'Ação'),
    ('Aventura', 'Aventura'),
    ('Animação', 'Animação'),
    ('Comédia', 'Comédia'),
    ('Crime', 'Crime'),
    ('Documentário', 'Documentário'),
    ('Drama', 'Drama'),
    ('Família', 'Família'),
    ('Fantasia', 'Fantasia'),
    ('Ficção Científica', 'Ficção Científica'),
    ('Guerra', 'Guerra'),
    ('História', 'História'),
    ('Mistério', 'Mistério'),
    ('Musical', 'Musical'),
    ('Romance', 'Romance'),
    ('Suspense', 'Suspense'),
    ('Terror', 'Terror'),
    ('Western', 'Western')
]

user_names = [
    ('Pedro Lucas', 'Pedro Lucas'),
    ('Sarah', 'Sarah')
]

rate_choices = [
    (0.0, 0.0),
    (0.5, 0.5),
    (1.0, 1.0),
    (1.5, 1.5),
    (2.0, 2.0),
    (2.5, 2.5),
    (3.0, 3.0),
    (3.5, 3.5),
    (4.0, 4.0),
    (4.5, 4.5),
    (5.0, 5.0),
]

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(choices=category_choices, max_length=24, unique=True)

    def __str__(self):
        return self.name

class Saga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=244, unique=True)

    def __str__(self):
        return self.name

from django.utils.translation import gettext_lazy as _

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    models.CharField(max_length=244, choices=user_names)
    name = models.CharField(max_length=244, unique=True, error_messages={
        'unique': _("Filme com este nome já existe.")
    })
    category = models.ManyToManyField(Category, related_name='movie_category')
    url = models.CharField(max_length=244, null=True)
    sinopse = models.CharField(max_length=488, null=True)
    img = models.FileField(upload_to='movieImgs/')
    watched = models.BooleanField(default=False)
    fk_saga = models.ForeignKey(Saga, related_name='saga_movie', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from django.utils import timezone

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_movie = models.ForeignKey(Movie, related_name='movie_session', on_delete=models.CASCADE)
    dt_session = models.DateTimeField(auto_now_add=True)

    @property
    def get_local_dt_session(self):
        return timezone.localtime(self.dt_session)
    
    @property
    def formated_dt_session(self):
        return timezone.localtime(self.dt_session).strftime("%d/%m/%Y, %H:%M")
    

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_user = models.ForeignKey(User, related_name='user_comment', null=True, on_delete=models.CASCADE)
    fk_movie = models.ForeignKey(Movie, related_name='movie_comment', null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=488)
    dt_comment = models.DateTimeField(null=True)

    @property
    def get_local_dt_comment(self):
        return timezone.localtime(self.dt_comment)
    
    @property
    def formated_dt_comment(self):
        return timezone.localtime(self.dt_comment).strftime("%d/%m/%Y, %H:%M")

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_user = models.ForeignKey(User, related_name='user_review', null=True, on_delete=models.CASCADE)
    rate = models.FloatField(default=0, choices=rate_choices)
    fk_movie = models.ForeignKey(Movie, related_name='movie_rate', null=False, on_delete=models.CASCADE)
    dt_review = models.DateTimeField(null=True)

    @property
    def get_local_dt_review(self):
        return timezone.localtime(self.dt_review)
    
    @property
    def formated_dt_review(self):
        return timezone.localtime(self.dt_review).strftime("%d/%m/%Y, %H:%M")