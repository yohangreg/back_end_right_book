#!/bin/bash

cd /app/backend  # Vai para o diretório onde o manage.py está localizado

# Inicia o servidor Django
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000  # Altere para 0.0.0.0 para aceitar conexões externas
