# Importa o módulo admin do Django para permitir a customização do painel
from django.contrib import admin
# Importa os modelos Category, Tag e Page
#  criados no arquivo models.py do seu app blog
from blog.models import Category, Tag, Page

# O decorator @admin.register vincula a classe TagAdmin 
# diretamente ao modelo Tag,
# dizendo ao Django que esta classe controlará 
# como as Tags aparecem no painel administrativo.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Define as colunas que serão exibidas 
    # na tabela de listagem das Tags no painel.
    list_display = 'id', 'name', 'slug',
    
    # Define quais dessas colunas serão links clicáveis 
    # para abrir o formulário de edição da Tag.
    list_display_links = 'name',
    
    # Adiciona uma barra de pesquisa que filtra as Tags por ID, Nome ou Slug.
    search_fields = 'id', 'name', 'slug',
    
    # Ativa a paginação na listagem, exibindo no máximo 10 Tags por página.
    list_per_page = 10
    
    # Define a ordenação padrão dos itens. O '-' antes do 'id' 
    # significa ordem decrescente (do mais novo para o mais antigo).
    ordering = '-id',
    
    # Faz com que o campo 'slug' seja preenchido automaticamente 
    # via JavaScript em tempo real 
    # enquanto você digita o 'name' no formulário de criação.
    prepopulated_fields = {
        "slug": ('name',),
    }


# Registra e customiza a exibição do modelo Category no painel administrativo.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Exibe o ID, Nome e Slug na tabela de categorias do painel.
    list_display = 'id', 'name', 'slug',
    
    # Permite clicar no Nome para editar a categoria.
    list_display_links = 'name',
    
    # Permite pesquisar categorias por ID, Nome ou Slug.
    search_fields = 'id', 'name', 'slug',
    
    # Limita a tabela a exibir 10 categorias por página.
    list_per_page = 10
    
    # Ordena as categorias exibindo os IDs maiores (mais recentes) primeiro.
    ordering = '-id',
    
    # Preenche o slug da categoria automaticamente com base no nome digitado.
    prepopulated_fields = {
        "slug": ('name',),
    }

# O @admin.register vincula o modelo 'Page' a 
# esta classe de configuração no painel administrativo
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    
    # Define quais campos (colunas) serão exibidos 
    # na tabela de listagem do painel
    list_display = 'id', 'title', 'is_published',
    
    # Define que o campo 'title' será um link clicável 
    # para abrir a tela de edição do registro
    list_display_links = 'title',
    
    # Cria uma barra de pesquisa que busca termos digitados 
    # dentro dos campos informados
    search_fields = 'id', 'slug', 'title', 'content',
    
    # Limita a exibição da listagem a 50 registros por página (cria paginação)
    list_per_page = 50
    
    # Adiciona um painel lateral de filtros baseados 
    # no campo 'is_published' (ex: Filtrar por Sim ou Não)
    list_filter = 'is_published',
    
    # Permite editar o campo 'is_published' com um clique diretamente 
    # na tabela de listagem, sem precisar abrir o registro
    list_editable = 'is_published',
    
    # Define a ordenação padrão dos registros. O '-' 
    # indica ordem decrescente (do maior ID para o menor)
    ordering = '-id',
    
    # Preenche o campo 'slug' automaticamente via JavaScript 
    # no navegador enquanto você digita o campo 'title'
    prepopulated_fields = {
        "slug": ('title',),
    }
