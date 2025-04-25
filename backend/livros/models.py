from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class Reviews(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    livro = models.CharField(max_length=255)  # Usando CharField com um limite de caracteres adequado
    nota = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # IntegerField convertido para PositiveSmallIntegerField
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-data_criacao']  # Ordena por data de criação, do mais recente para o mais antigo

    def __str__(self):
        return f"{self.usuario.username} - {self.livro} ({self.nota})"
    
class WishList(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_list")
    livro = models.CharField(max_length=255)  # Usando CharField com um limite de caracteres adequado

    def __str__(self):
        return f"{self}"