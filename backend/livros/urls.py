from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registrar_usuario, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('update/', views.update_usuario, name='update'),
]

urlpatterns += [
    path('search/user/', views.buscar_username, name='buscar_username'),
]

urlpatterns += [
    path('search-book', views.buscar_livro, name='buscar_livro'),
    path('search-book/<str:id>/', views.buscar_id, name='buscar_id'),
]

urlpatterns += [
    path('search/reviews/users/<int:id>', views.buscar_avaliacoes_por_usuario, name='buscar_avaliacoes_por_usuario'),
    path('search/reviews/books/<str:id>', views.buscar_avaliacoes_por_livro, name='buscar_avaliacoes_por_livro'),
]

