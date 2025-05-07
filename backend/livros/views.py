import os
import requests
from .models import Reviews, WishList
from .serializers import ReviewsSerializer, UserSerializer, WishListSerializer
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import status, viewsets 
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

GOOGLE_BOOKS_API_URL = os.getenv("GOOGLE_BOOKS_API_URL")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    email = request.data.get("email")
    username = request.data.get("username")
    password = request.data.get("password")

    if not email or not username or not password:
        return Response({"error": "Preencha todos os campos"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email já existe"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(email=email, username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

    return Response({"error": "Credenciais inválidas"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_usuario(request):
    user = request.user
    email = request.data.get("email", user.email)
    username = request.data.get("username", user.username)
    password = request.data.get("password")

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response({"error": "Você não pode usar um email que pertence a outro usuário."}, status=status.HTTP_403_FORBIDDEN)
    
    if User.objects.exclude(id=user.id).filter(username=username).exists():
        return Response({"error": "Você não pode usar um nome de usuário que pertence a outro usuário."}, status=status.HTTP_403_FORBIDDEN)

    user.email = email
    user.username = username
    
    if password:
        user.set_password(password)
    
    user.save()
    return Response({"message": "Usuário atualizado com sucesso"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_usuario(request):
    try:
        token = request.auth
        if token:
            token.delete()
            return Response({"message": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Token inválido ou não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Erro ao realizar logout: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_username(request):
    username = request.query_params.get("username")  # Obtém o username da query string

    if not username:
        return Response({"error": "O parâmetro 'username' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()

    if not user:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "data_criacao": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        "ultimo_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "Nunca logou",
    }

    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_livros_relevantes(request):
    # Parâmetros de paginação
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 20))

    if page < 1 or page_size < 1:
        return Response({"error": "page e page_size devem ser maiores que 0."}, status=status.HTTP_400_BAD_REQUEST)

    start_index = (page - 1) * page_size

    params = {
        "q": "+populares",  # Palavra-chave genérica para popularidade
        "orderBy": "relevance",
        "startIndex": start_index,
        "maxResults": page_size,
        "langRestrict": "pt",  # Apenas livros em português
        "key": GOOGLE_BOOKS_API_KEY
    }

    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        livros_formatados = []

        for livro in data.get("items", []):
            nota = search_review_by_book(livro.get("id"))
            volume_info = livro.get("volumeInfo", {})
            livros_formatados.append({
                "id": livro.get("id"),
                "isbn": volume_info.get("industryIdentifiers", "ISBNs não informados"),
                "titulo": volume_info.get("title", "Título não disponível"),
                "autores": volume_info.get("authors", ["Autor desconhecido"]),
                "descricao": volume_info.get("description", "Sem descrição"),
                "data_publicacao": volume_info.get("publishedDate", "Data não disponível"),
                "paginas": volume_info.get("pageCount", "Não informado"),
                "categorias": volume_info.get("categories", []),
                "imagem": volume_info.get("imageLinks", {}).get("thumbnail", None),
                "nota": nota
            })

        return Response({
            "pagina_atual": page,
            "tamanho_pagina": page_size,
            "total_itens": data.get("totalItems", 0),
            "livros": livros_formatados
        }, status=status.HTTP_200_OK)

    return Response({"error": "Erro ao buscar livros."}, status=response.status_code)

def search_review_by_book(id):
    avg_nota = Reviews.objects.filter(livro=id).aggregate(media=Avg('nota'))['media']
    return round(avg_nota) if avg_nota is not None else None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_livro(request):
    # Obtém os parâmetros de busca
    titulo = request.query_params.get("titulo")
    autor = request.query_params.get("autor")
    isbn = request.query_params.get("isbn")
    categoria = request.query_params.get("categoria")
    
    # Constrói a query de pesquisa para a API do Google Books
    query = []
    if titulo:
        query.append(f"intitle:{titulo}")
    if autor:
        query.append(f"inauthor:{autor}")
    if isbn:
        query.append(f"isbn:{isbn}")
    if categoria:
        query.append(f"subject:{categoria}")

    if not query:
        return Response({"error": "Pelo menos um parâmetro de busca (titulo, autor, isbn, categoria) é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Junta todos os parâmetros de pesquisa
    query_string = "+".join(query)
    
    params = {
        "q": query_string,
        "key": GOOGLE_BOOKS_API_KEY
    }

    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" not in data:
            return Response({"error": "Nenhum livro encontrado para os parâmetros fornecidos."}, status=status.HTTP_404_NOT_FOUND)

        livros_formatados = []
        for livro in data["items"]:
            volume_info = livro["volumeInfo"]
            livros_formatados.append({
                "id": livro.get("id"),
                "isbn": volume_info.get("industryIdentifiers", "ISBNs não informados"),
                "titulo": volume_info.get("title", "Título não disponível"),
                "autores": volume_info.get("authors", ["Autor desconhecido"]),
                "descricao": volume_info.get("description", "Sem descrição"),
                "data_publicacao": volume_info.get("publishedDate", "Data não disponível"),
                "paginas": volume_info.get("pageCount", "Não informado"),
                "categorias": volume_info.get("categories", []),
                "imagem": volume_info.get("imageLinks", {}).get("thumbnail", None)
            })

        return Response(livros_formatados, status=status.HTTP_200_OK)
    
    return Response({"error": "Erro ao buscar livros."}, status=response.status_code)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_id(request, id):
    """
    Busca um livro pelo ID na API do Google Books e retorna informações formatadas.
    """
    headers = {
        "key": GOOGLE_BOOKS_API_KEY
    }
    response = requests.get(f"{GOOGLE_BOOKS_API_URL}/{id}", headers=headers)

    if response.status_code != 200:
        return Response({"error": "Erro ao buscar livro."}, status=response.status_code)
    
    data = response.json()
    volume_info = data.get("volumeInfo", {})
    
    livro_formatado = {
        "id": data.get("id"),
        "titulo": volume_info.get("title", "Título não disponível"),
        "autores": volume_info.get("authors", ["Autor desconhecido"]),
        "descricao": volume_info.get("description", "Sem descrição"),
        "data_publicacao": volume_info.get("publishedDate", "Data não disponível"),
        "paginas": volume_info.get("pageCount", "Não informado"),
        "categorias": volume_info.get("categories", []),
        "imagem": volume_info.get("imageLinks", {}).get("thumbnail", None)
    }
    
    return Response(livro_formatado, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_avaliacoes_por_usuario(request, id):

    if not id:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    
    reviews = Reviews.objects.filter(usuario=id)

    if not reviews.exists():
        return Response({"error": "Nenhuma avaliação encontrada para este usuário"}, status=status.HTTP_404_NOT_FOUND)
    
    serialized_reviews = ReviewsSerializer(reviews, many=True)

    return Response(serialized_reviews.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_avaliacoes_por_livro(request, id):

    if not id:
        return Response({"error": "Livro não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    
    reviews = Reviews.objects.filter(livro=id)

    if not reviews.exists():
        return Response({"error": "Nenhuma avaliação encontrada para este livro"}, status=status.HTTP_404_NOT_FOUND)
    
    serialized_reviews = ReviewsSerializer(reviews, many=True)

    return Response(serialized_reviews.data, status=status.HTTP_200_OK)