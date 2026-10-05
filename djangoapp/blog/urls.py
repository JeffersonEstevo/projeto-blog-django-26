# Importa a função da view 'index' 
# criada no arquivo views.py do seu aplicativo blog

# É necessário importar as views do arquivo views.py do app 'blog'.
# Sem esses imports, o Django não saberia quais classes 
# executar quando o usuário acessasse as respectivas URLs.
# Importação de classes baseadas em views (CBVs) para gerenciar 
# listagens (categorias, criadores, posts, buscas, tags) 
# e detalhes (páginas, posts)
from blog.views import (CategoryListView, CreatedByListView, PageDetailView,
                        PostDetailView, PostListView, SearchListView,
                        TagListView)

# Importa a função 'path' do Django, 
# necessária para mapear as rotas de URL para as views correspondentes
from django.urls import path

# Define o namespace do aplicativo para organizar as URLs e 
# permitir o uso de rotas reversas seguras como 'blog:index'
app_name = 'blog'

# Lista que armazena todas as rotas de URL específicas deste aplicativo
urlpatterns = [
    
    # Rota para a página inicial (raiz) do site.
    # O caminho vazio ('') indica a URL base (ex: meudominio.com/).
    # A classe PostListView é convertida em view pelo .as_view() 
    # para listar os posts.
    # O parâmetro name='index' permite referenciar esta URL 
    # facilmente em templates e códigos.
    path('', PostListView.as_view(), name='index'),

    # Define que se o usuário acessar 'seusite.com/post/<slug>/', 
    # o Django chama a Class-Based View 'PostDetailView'.
    # O argumento name='post' serve para 
    # você referenciar essa URL nos templates ou views 
    # sem precisar escrever o caminho manualmente (URL Reverse).
    # Rota para a página de um post específico: 
    # captura um texto amigável (slug) da URL, 
    # envia para a view 'PostDetailView' e dá o nome de 'post' para essa rota.
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),

    # Faz o mesmo que o de cima: mapeia o endereço 
    # 'seusite.com/page/' para a função 'page'.
    # path('page/', page, name='page'),


    # Acessa uma página específica com base no seu 'slug' 
    # (um texto amigável para URLs, ex: /page/politica-de-privacidade/)
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),

    # Filtra e exibe conteúdos criados por um autor específico 
    # usando o ID numérico dele (ex: /created_by/5/)
    path(
        'created_by/<int:author_pk>/',
        CreatedByListView.as_view(),
        name='created_by'
    ),

    # A classe CategoryListView é convertida em view pelo .as_view()
    # Exibe posts ou produtos de uma categoria específica 
    # usando o 'slug' dela (ex: /category/tecnologia/)
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),

    # Define a rota para filtrar posts por tag:
    # 1. 'tag/<slug:slug>/' -> Captura o identificador amigável da tag na URL 
    # (ex: /tag/python/)
    # 2. tag                -> Função/View que será executada 
    # quando a URL for acessada
    # 3. name='tag'         -> Nome de identificação da rota 
    # (usado pelo {% url 'blog:tag' ... %})
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),

    # Define a rota para a página de busca:
    # 1. 'search/' -> Define o caminho URL padrão 
    # para a funcionalidade de pesquisa (ex: /search/)
    # 2. search    -> Função/View que processará a consulta e 
    # retornará os resultados quando a URL for acessada
    # 3. name='search' -> Nome de identificação da rota 
    # (usado pelo {% url 'blog:search' ... %})
    path('search/', SearchListView.as_view(), name='search'),
]
