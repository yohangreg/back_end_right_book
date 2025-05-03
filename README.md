# 📚 RightBook API

A **RightBook** é uma API RESTful desenvolvida com Django e Django REST Framework para gerenciamento de avaliações de livros, listas de desejos e integração com a Google Books API.

---

## 🚀 Funcionalidades

- Registro e login de usuários com autenticação via token.
- Avaliação de livros com nota e comentário.
- Lista de desejos pessoal para cada usuário.
- Busca de livros via Google Books API (por título, autor, ISBN ou categoria).
- CRUD completo de reviews e wishlist.
- Permissões configuradas para garantir segurança e integridade dos dados.

---

## 🧠 Tecnologias utilizadas

- Python 3.11+
- Django 5.1+
- Django REST Framework
- PostgreSQL
- Google Books API
- dotenv (para variáveis de ambiente)
- CORS Headers

---

## 🧪 Instalação

```bash
# Clone o repositório
git clone https://github.com/yohangreg/back_end_right_book.git

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o .env
cp .env.example .env  # edite com suas credenciais

# Execute as migrações
python manage.py migrate

# Crie superusuário (opcional)
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

---

## 🐳 Rodando com Docker (alternativa)

Se preferir rodar a aplicação com Docker, siga os passos abaixo:

### Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### ⚙️ Configuração

1. **Configure seu arquivo `.env`**:  
   Copie o arquivo de exemplo e edite com suas variáveis de ambiente:

   ```bash
   cp .env.example .env
   ```

2. **Build e subida dos containers**:

   ```bash
   docker-compose up --build
   ```

   Isso irá:
   - Construir a imagem da aplicação
   - Subir o container da API
   - A API ficará acessível em `http://localhost:8000`

### 🔄 Comandos úteis

- Parar os containers:
  ```bash
  docker-compose down
  ```

- Subir sem rebuild:
  ```bash
  docker-compose up
  ```