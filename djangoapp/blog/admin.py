# Importa o módulo admin do Django para permitir a customização do painel
from django.contrib import admin
# Importa os modelos Category, Tag, Page e Post
#  criados no arquivo models.py do seu app blog
from blog.models import Category, Tag, Page, Post

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

# O decorador vincula o modelo 'Post' a esta classe de configuração 
# personalizada no admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    # Define as colunas que serão exibidas na tabela de listagem dos posts
    list_display = 'id', 'title', 'is_published', 'created_by',
    
    # Transforma o campo 'title' em um link clicável para abrir 
    # o formulário de edição do post
    list_display_links = 'title',
    
    # Cria uma barra de pesquisa capaz de buscar termos 
    # dentro desses campos específicos
    search_fields = 'id', 'slug', 'title', 'excerpt', 'content',
    
    # Limita a listagem a no máximo 50 posts por página, 
    # criando uma paginação automática
    list_per_page = 50
    
    # Adiciona um painel lateral de filtros para segmentar os posts 
    # por 'category' e por status 'is_published'
    list_filter = 'category', 'is_published',
    
    # Permite ativar/desativar a publicação (is_published) 
    # com um clique direto na tabela de listagem
    list_editable = 'is_published',
    
    # Define a ordenação padrão dos posts na lista. O '-' 
    # indica ordem decrescente (do ID mais novo para o mais antigo)
    ordering = '-id',
    
    # Define campos que serão apenas para leitura, 
    # impedindo que o usuário os altere manualmente no formulário
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by',
    
    # Preenche o campo 'slug' de forma automática via JavaScript 
    # enquanto você digita o 'title' no formulário
    prepopulated_fields = {
        "slug": ('title',),
    }
    
    # Transforma os campos de relacionamento 
    # (Chave Estrangeira/Many-to-Many) em caixas de busca assíncronas.
    # Evita o travamento da página caso você tenha 
    # milhares de tags ou categorias cadastradas.
    # Nota: Para funcionar, os admins de 'Tag' e 'Category' 
    # precisam ter o 'search_fields' configurado.
    autocomplete_fields = 'tags', 'category',

def save_model(self, request, obj, form, change):
    # O Django passa o booleano 'change' como True se 
    # o objeto já existe (está sendo editado)
    # ou False se o objeto está sendo criado do zero.
    if change:
        # Se o objeto já existia, define o usuário atual 
        # como o responsável pela atualização
        obj.updated_by = request.user  # type: ignore
    else:
        # Se for um novo registro, define o usuário atual como o criador
        obj.created_by = request.user  # type: ignore

    # Salva efetivamente as alterações no banco de dados
    obj.save()
