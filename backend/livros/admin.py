from django.contrib import admin
from .models import Reviews

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("usuario", "livro", "nota", "data_criacao")  # Campos que serão exibidos na listagem
    list_filter = ("nota", "data_criacao")  # Filtros laterais
    search_fields = ("usuario__username", "livro", "comentario")  # Campos pesquisáveis