from django.core.management.base import BaseCommand
from filmes.models import Category

class Command(BaseCommand):
    help = 'Popula o banco de dados com as categorias'

    def handle(self, *args, **kwargs):
        category_choices = [
            'Ação', 'Aventura', 'Animação', 'Comédia', 'Crime',
            'Documentário', 'Drama', 'Família', 'Fantasia', 
            'Ficção Científica', 'Guerra', 'História', 'Mistério',
            'Musical', 'Romance', 'Suspense', 'Terror', 'Western'
        ]

        for category in category_choices:
            Category.objects.get_or_create(name=category)
            self.stdout.write(self.style.SUCCESS(f'Categoria "{category}" adicionada.'))

        self.stdout.write(self.style.SUCCESS('Todas as categorias foram adicionadas com sucesso!'))
