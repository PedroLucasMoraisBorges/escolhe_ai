from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .forms import *

import random
from django.utils import timezone

def getErrors(Forms):
    errors = []
    for form in Forms:
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{error}")
    return errors
    
# Create your views here.
class HomePage(View):
    def get(self, request):
        return render(request, 'homePage.html')
    
class Movies(View):
    def get(self, request):
        movies = Movie.objects.filter()

        context = {
            'movies' : movies
        }
        
        return render(request, 'movies.html', context)

class RegisterMovie(View):
    def get(self, request):
        movieForm = MovieForm()
        sagaForm = SagaForm()

        context = {
            'movieForm' : movieForm,
            'sagaForm' : sagaForm
        }

        return render(request, 'registerMovie.html', context)
    
    def post(self, request):
        movieForm = MovieForm(request.POST, request.FILES)
        sagaForm = SagaForm()

        if movieForm.is_valid():
            movieForm.save()
            return redirect('movies')
        
        context = {
            'movieForm' : movieForm,
            'sagaForm' : sagaForm,
            'errors' : getErrors([movieForm])
        }

        return render(request, 'registerMovie.html', context)

class EditMovie(View):
    def get(self, request, id):
        movie = Movie.objects.get(id=id)
        saga = movie.fk_saga

        movieForm = MovieForm(instance=movie)
        sagaForm = SagaForm(instance=saga)

        context = {
            'movieForm' : movieForm,
            'sagaForm' : sagaForm,
            'movie' : movie
        }

        return render(request, 'editMovie.html', context)
    
    def post(self, request, id):
        movie = Movie.objects.get(id=id)
        movieForm = MovieForm(request.POST, request.FILES, instance=movie)
        sagaForm = SagaForm()

        if movieForm.is_valid():
            if movieForm.has_changed():
                movieForm.save()
            return redirect('movies')
        
        context = {
            'movieForm' : movieForm,
            'sagaForm' : sagaForm
        }
        return render(request, 'registerMovie.html', context)

class RegisterSagaAPI(APIView):
    def post(self, request):
        sagaForm = SagaForm(request.POST)

        if sagaForm.is_valid():
            saga = sagaForm.save()
            return Response({
                "id": saga.id,
                "name": saga.name,
            }, status=status.HTTP_201_CREATED)


        return Response({
            "errors": sagaForm.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class MoviePage(View):
    def get(self, request, id):
        movie = Movie.objects.get(id=id)
        reviews = Review.objects.filter(fk_movie=movie)
        comments = Comment.objects.filter(fk_movie=movie)

        if reviews.exists():
            averageReview = sum(review.rate for review in reviews) / reviews.count()
        else:
            averageReview = 0  # Caso não tenha reviews

        returnComments = []
        for comment in comments:
            reviewComent = Review.objects.get(fk_user=comment.fk_user, dt_review=comment.dt_comment, fk_movie=comment.fk_movie)
            returnComments.append({
                'comment' : comment,
                'review' : reviewComent
            })
        
        session = Session.objects.filter(fk_movie=movie).order_by('-dt_session').first()


        context = {
            'movie': movie,
            'averageReview': round(averageReview, 1),
            'comments' : returnComments,
            'reviewForm' : ReviewForm(),
            'commentForm' : CommentForm(),
            'lastSession' : session
        }

        return render(request, 'moviePage.html', context)

    def post(self, request, id):
        movie = Movie.objects.get(id=id)

        reviewForm = ReviewForm(request.POST)
        commentForm = CommentForm(request.POST)

        date = timezone.now()

        if reviewForm.is_valid() and commentForm.is_valid():
            review = reviewForm.save(commit=False)
            review.fk_movie = movie
            review.fk_user = request.user
            review.dt_review = date
            review.save()

            comment = commentForm.save(commit=False)
            comment.fk_movie = movie
            comment.fk_user = request.user
            comment.dt_comment = date
            comment.save()

            return redirect('movie_page', id=id)
    
class MovieGiveaway(View):
    def get(self, request):
        form = RandomMovieForm()

        context = {
            'form' : form
        }

        return render(request, 'MovieGiveawayPage.html', context)
    
    def post(self, request):
        is_whatched = request.POST.get('is_whatched')
        gender = request.POST.get('gender')
        rating = request.POST.get('rating')
        query = Q()

        if gender != '':
            category = Category.objects.get(name=gender)
            query &= Q(category=category)

        if is_whatched == 'True':
            query &= Q(watched=True)
        elif is_whatched == 'False':
            query &= Q(watched=False)

        if query:
            movies = Movie.objects.filter(query)
        else:
            movies = Movie.objects.filter()
        
        returnMovies = []

        if rating != '' and is_whatched == 'True':
            for movie in movies:
                rates = Review.objects.filter(fk_movie = movie)
                sum = 0
                count = 0

                for rate in rates:
                    sum += rate.rate
                    count += 1
                
                
                average = sum/count

                if int(rating) > average:
                    returnMovies.append(movie)
        
        if returnMovies:
            movies = returnMovies

        movie = random.choice(movies)
        
        categories = ''

        for category in movie.category.all():
            categories += f' {category.name},'

        categories = categories[1:-1]

        context = {
            'form' : RandomMovieForm(request.POST),
            'movie' : movie,
            'categories' : categories
        }

        return render(request, 'MovieGiveawayPage.html', context)
    
class MarkAsWatched(APIView):
    def get(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            movie.watched = True
            movie.save()

            # Obtendo a data atual sem a hora
            today = timezone.now().date()

            # Verificando se já existe uma sessão para o filme no dia de hoje
            if Session.objects.filter(fk_movie=movie, dt_session__date=today).exists():
                return Response({
                    "errors": "Já existe uma sessão cadastrada hoje"
                }, status=status.HTTP_200_OK)

            # Caso não exista, cria a sessão
            session = Session.objects.create(
                fk_movie=movie
            )

            return Response({
                "session": session.get_local_dt_session.strftime("%d/%m/%Y, %H:%M"),
                "name": movie.name,
            }, status=status.HTTP_201_CREATED)

        except Movie.DoesNotExist:
            return Response({
                "errors": "Filme não encontrado"
            }, status=status.HTTP_400_BAD_REQUEST)
