#!/bin/sh
# Coleta todos os arquivos estáticos do Django (CSS, JS, Imagens) e os agrupa no diretório configurado em STATIC_ROOT.
python manage.py collectstatic --noinput