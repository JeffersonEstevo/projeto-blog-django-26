# Importa a função da view 'index' 
# criada no arquivo views.py do seu aplicativo blog
from blog.views import index

# Importa a função 'path' do Django, 
# necessária para mapear as rotas de URL para as views correspondentes
from django.urls import path

# Define o namespace do aplicativo para organizar as URLs e 
# permitir o uso de rotas reversas seguras como 'blog:index'
app_name = 'blog'

# Lista que armazena todas as rotas de URL específicas deste aplicativo
urlpatterns = [
    
    # Cria uma rota para a página inicial do app (URL vazia ''), 
    # chama a view 'index' e dá o nome de 'index' para o link
    path('', index, name='index'),
]
