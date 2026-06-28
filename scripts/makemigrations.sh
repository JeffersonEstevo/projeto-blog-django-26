#!/bin/sh
echo 'Executando makemigrations.sh'
# Cria os arquivos de migração com base nas alterações feitas nos models do Django.
python manage.py makemigrations --noinput