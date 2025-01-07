from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Saga)
admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Category)