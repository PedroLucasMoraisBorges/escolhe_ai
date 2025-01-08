from django.urls import path
from .views import *

urlpatterns = [
    path('', Movies.as_view(), name='movies'),
    path('cadastarFilme/', RegisterMovie.as_view(), name='register_movie'),
    path('editarFilme/<str:id>', EditMovie.as_view(), name='edit_movie'),
    path('sortarFilme/', MovieGiveaway.as_view(), name='movie_giveaway'),
    path('paginaDoFilme/<str:id>', MoviePage.as_view(), name='movie_page'),

    # APIS

    path('registerSagaAPI/', RegisterSagaAPI.as_view(), name='register_saga_api'),
    path('marcarComoAssistido/<str:id>', MarkAsWatched.as_view(), name='mark_as_whatched'),
]