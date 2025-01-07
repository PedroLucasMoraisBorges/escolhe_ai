from django import forms
from .models import *

class MovieForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='Nome*',
        widget=forms.TextInput(attrs={
            'placeholder' : 'Nome do filme'
        })
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget= forms.SelectMultiple(attrs={'class':'form-control input-search'}),
        label='Gênero*',
        required=True
    )

    img = forms.ImageField(
        label='Imagem*',
        required=True,
        widget=forms.FileInput(
            attrs={
                'onchange': 'previewImage(event)',
                'accept' : '.jpg, .png'
            }
        ),
    )

    sinopse = forms.CharField(
        label='Sinopse*',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder' : 'Informe uma síntese do filme'
        })
    )

    url = forms.CharField(
        label='URL',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder' : 'URL do IMDB'
        })
    )

    fk_saga = forms.ModelChoiceField(
        queryset=Saga.objects.all(),
        label='Saga'
    )

    class Meta:
        model=Movie
        fields = ['name', 'category', 'img', 'fk_saga', 'sinopse', 'url']

class SagaForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome da saga',
        required=True
    )

    class Meta:
        model=Saga
        fields=['name']

class RandomMovieForm(forms.Form):
    status_choices = [
        ('', 'Qualquer um'),
        (True, 'Já assistido'),
        (False, 'Nunca assistido')
    ]

    rating_choices = [
        ('', 'Nota Mínima'),
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    is_whatched = forms.ChoiceField(
        required=False,
        choices=status_choices,
        widget=forms.Select()
    )

    rating = forms.ChoiceField(
        required=False,
        choices=rating_choices,
        widget=forms.Select()
    )

    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'Selecione o gênero')] + category_choices,
        widget=forms.Select()
    )

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        label='Comentário',
        widget=forms.Textarea()
    )

    class Meta:
        model=Comment
        fields=['text']

class ReviewForm(forms.ModelForm):
    rate = forms.ChoiceField(
        required=True,
        label='Avalie o Filme',
        choices=[('' , 'Dê a sua nota')] + rate_choices,
        widget=forms.Select()
    )

    class Meta:
        model=Review
        fields=['rate']