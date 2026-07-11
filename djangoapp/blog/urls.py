# Importa a função da view 'index' 
# criada no arquivo views.py do seu aplicativo blog

# É necessário importar as funções (ou classes) 'page' e 'post' do arquivo views.py do app 'blog'.
# Sem esse import, o Django não saberia qual função executar quando o usuário acessasse a URL.
from blog.views import index, page, post

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

    # Define que se o usuário acessar 'seusite.com/post/', o Django chama a função 'post'.
    # O argumento name='post' serve para você referenciar essa URL nos templates ou views 
    # sem precisar escrever o caminho "post/" manualmente (URL Reverse).
    path('post/', post, name='post'),

    # Rota para a página de um post específico: captura um texto amigável (slug) da URL, 
    # envia para a view 'post' e dá o nome de 'post' para essa rota.
    path('post/<slug:slug>/', post, name='post'),

    # Faz o mesmo que o de cima: mapeia o endereço 'seusite.com/page/' para a função 'page'.
    path('page/', page, name='page'),
]
