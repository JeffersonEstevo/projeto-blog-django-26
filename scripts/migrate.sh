#!/bin/sh
# Sempre executa makemigrations.sh anteriormente
makemigrations.sh
echo 'Executando migrate.sh'
# Aplica as migrações do banco de dados (cria/atualiza as tabelas de acordo com seus models do Django).
python manage.py migrate --noinput