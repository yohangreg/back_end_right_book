FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Defina o diretório de trabalho como o diretório onde o manage.py está localizado
WORKDIR /app

# Copia todos os arquivos do projeto, incluindo o .env, para dentro do container
COPY . /app

# Instala as dependências
RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

# Permite execução do script de entrypoint
RUN chmod +x /app/entrypoint.sh

# Expõe a porta padrão do Django
EXPOSE 8000

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
