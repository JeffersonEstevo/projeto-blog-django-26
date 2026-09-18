# É necessário importar a função render, que é um atalho do Django para 
# juntar um arquivo HTML (template) com os dados do banco de dados e 
# entregar ao navegador.
# Importa atalhos do Django para redirecionamento e renderização de templates
from django.shortcuts import render

# Importa o modelo (tabela) 'Post' do app 'blog' 
# Importa o modelo (tabela) 'Page' do app 'blog' 
# para poder consultar os dados do banco
from blog.models import Page, Post

# Importa o modelo padrão de Usuário do Django para gerenciar contas, 
# autenticação e dados de usuários no sistema.
from django.contrib.auth.models import User

# Importa a exceção Http404 para disparar uma página de erro 404 
# (Página Não Encontrada) quando um registro não for encontrado.
# Importa exceções HTTP (como o 404) e classes de requisição/resposta do Django
from django.http import Http404

# Importa a classe do Django responsável por 
# gerenciar a divisão de dados em páginas
from django.core.paginator import Paginator

# Importa a classe Q do Django, permitindo criar consultas complexas 
# com operadores lógicos (como o OU / OR)
from django.db.models import Q

# Importa a classe ListView genérica do Django para criar visualizações 
# baseadas em classe focadas em listar registros de um modelo 
# (ex: listar posts, produtos, usuários).
from django.views.generic import ListView

# Importa o tipo Any para fins de tipagem estática (Type Hinting)
from typing import Any  

# Importa a classe QuerySet do Django para tipagem de consultas ao banco
from django.db.models.query import QuerySet  


# Define uma constante com o número máximo de posts 
# que serão exibidos em cada página
PER_PAGE = 9

# Define a classe da view baseada em classe (CBV) chamada 'PostListView', 
# herdando de 'ListView' do Django para lidar automaticamente 
# com a listagem de registros
class PostListView(ListView):
    # Caminho do template HTML que será renderizado para exibir esta página
    template_name = 'blog/pages/index.html'
    
    # Nome da variável de contexto usada no template para 
    # acessar a lista de itens
    context_object_name = 'posts'
    
    # Quantidade de itens exibidos por página (habilita a paginação)
    paginate_by = PER_PAGE
    
    # Function Based Views -> São funções
    # Class Based Views -> são classes (POOs)
    # Para mais informações consultar:
    # https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/

    # Chama o gerenciador customizado do modelo Post, 
    # executa o método get_published() 
    # (que filtra os publicados e ordena por ID decrescente) 
    # e armazena o resultado na variável 'queryset'.
    queryset = Post.objects.get_published()

    # Sobrescreve o método get_context_data para adicionar variáveis 
    # personalizadas ao contexto enviado ao template
    def get_context_data(self, **kwargs):
        # Obtém o dicionário de contexto padrão que o Django já prepara 
        # (incluindo a lista de posts, página atual, etc.)
        context = super().get_context_data(**kwargs)

        # Atualiza o dicionário de contexto adicionando 
        # uma nova variável chamada 'page_title' com o valor 'Home - '
        context.update({ 
            'page_title': 'Home - ',
        })
        
        # Retorna o contexto atualizado para que o template HTML 
        # possa utilizá-lo (ex: {{ page_title }})
        return context

def created_by(request, author_pk):
    # Busca o usuário no banco de dados 
    # utilizando a chave primária (pk) recebida. 
    # O método .first() retorna o primeiro objeto encontrado 
    # ou None se não existir.
    user = User.objects.filter(pk=author_pk).first()

    # Verifica se o usuário não foi encontrado no banco de dados. 
    # Se for None, interrompe a execução e 
    # retorna um erro 404 (Página Não Encontrada).
    if user is None:
        raise Http404()

    # Busca no banco de dados apenas os posts publicados 
    # que pertencem ao autor com o ID (pk) recebido
    posts = Post.objects.get_published()\
        .filter(created_by__pk=author_pk)

    # Define o nome padrão para exibição como sendo o username 
    # (nome de usuário).
    user_full_name = user.username

    # Verifica se o usuário possui um primeiro nome cadastrado. 
    # Se tiver, sobrescreve user_full_name combinando 
    # o primeiro e o último nome.
    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'
    # Cria o título personalizado da página combinando 
    # o nome do autor com um texto padrão.
    page_title = 'Posts de ' + user_full_name + ' - '

    # Configura a paginação, definindo quantos posts serão exibidos por página 
    # (baseado na constante PER_PAGE)
    paginator = Paginator(posts, PER_PAGE)
    
    # Pega o número da página atual direto da URL (ex: ?page=2). 
    # Se não houver, assume a página 1
    page_number = request.GET.get("page")
    
    # Recupera os posts específicos daquela página atual para enviar ao template
    page_obj = paginator.get_page(page_number)

    # Renderiza o template 'index.html' passando o objeto da página 
    # (com os posts filtrados e paginados)
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            # Passa a variável page_title dentro do dicionário de contexto 
            # para ser renderizada no template HTML.
            'page_title': page_title,
        }
    )

# Define uma View baseada em classe (CBV) personalizada que 
# herda de PostListView
class CreatedByListView(PostListView):  
    # Método construtor (inicializador) da classe
    def __init__(self, **kwargs: Any) -> None:  
        # Executa o construtor da classe pai (PostListView) para 
        # garantir inicializações padrão
        super().__init__(**kwargs)  
        # Cria um dicionário interno na instância para armazenar dados 
        # temporários entre os métodos da view
        self._temp_context: dict[str, Any] = {}  

    # Sobrescreve o método do Django responsável por 
    # enviar dados (contexto) para o template HTML 
    # [verificar ordem de sobrescrita na documentação]
    def get_context_data(self, **kwargs):  
        # Obtém o dicionário de contexto padrão gerado pela classe pai
        ctx = super().get_context_data(**kwargs)  
        # Recupera o objeto de usuário armazenado previamente 
        # no dicionário temporário
        user = self._temp_context['user']  
        # Define uma string padrão para o nome completo 
        # utilizando o username do usuário
        user_full_name = user.username  

        # Verifica se o usuário possui um primeiro nome preenchido no cadastro
        if user.first_name:  
            # Se tiver, substitui pelo nome e sobrenome combinados
            user_full_name = f'{user.first_name} {user.last_name}' 
        # Monta uma string customizada para o título da página baseada no autor    
        page_title = 'Posts de ' + user_full_name + ' - ' 
        # Atualiza o dicionário de contexto existente com novos dados
        ctx.update({  
             # Adiciona a variável 'page_title' 
             # para que ela possa ser exibida no template
            'page_title': page_title, 
        })
        # Retorna o dicionário de contexto finalizado para a renderização
        return ctx  

    # Sobrescreve o método do Django que define 
    # quais dados do banco serão buscados
    def get_queryset(self) -> QuerySet[Any]:  
        # Obtém o QuerySet básico inicial fornecido pela classe pai
        qs = super().get_queryset()  
        # Aplica um filtro no banco para trazer apenas os posts 
        # cujo criador tenha o mesmo ID (pk) do usuário armazenado
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)  
        # Retorna o QuerySet filtrado com os posts específicos do autor
        return qs  

    # Sobrescreve o método HTTP GET do Django para interceptar a requisição 
    # antes de processar a view
    def get(self, request, *args, **kwargs):  
        # Extrai o parâmetro 'author_pk' enviado através da URL 
        # (capturado nas chaves da rota)
        author_pk = self.kwargs.get('author_pk')  
        # Consulta o banco de dados buscando o usuário com aquele ID, 
        # retornando o primeiro encontrado (ou None)
        user = User.objects.filter(pk=author_pk).first()  

        # Verifica se o usuário consultado não existe no banco de dados
        if user is None:  
            # Se não existir, interrompe o fluxo imediatamente e 
            # exibe uma página de Erro 404 (Não Encontrado) padrão do Django
            raise Http404()  

        # Salva os dados validados do autor no dicionário temporário 
        # criado no __init__
        self._temp_context.update({  
            # Armazena o ID numérico do autor
            'author_pk': author_pk,  
            # Armazena o objeto completo do usuário encontrado
            'user': user,  
        })
        # Devolve o controle para o método get() original da classe pai 
        # para prosseguir com o ciclo de vida normal da view
        return super().get(request, *args, **kwargs)  

# Define uma View baseada em classe (CBV) personalizada para 
# listar posts filtrados por categoria, herdando de PostListView
class CategoryListView(PostListView):
    # Define que, caso a consulta não retorne nenhum objeto, 
    # o Django exibirá uma página 404 em vez de uma lista vazia
    allow_empty = False

    # Sobrescreve o método responsável por definir o conjunto de dados 
    # (queryset) que será consultado no banco de dados
    def get_queryset(self) -> QuerySet[Any]:
        # Obtém o queryset padrão da classe pai e o filtra para retornar 
        # apenas os posts cuja categoria corresponda ao slug passado na URL
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    # Sobrescreve o método do Django responsável por 
    # enviar dados (contexto) para o template HTML
    def get_context_data(self, **kwargs):
        # Obtém o dicionário de contexto padrão gerado pela classe pai
        ctx = super().get_context_data(**kwargs)
        
        # Monta uma string customizada para o título da página 
        # utilizando o nome da categoria obtida através do primeiro post listado
        page_title = (
            f'{self.object_list[0].category.name}'  # type: ignore
            ' - Categoria - '
        )
        
        # Atualiza o dicionário de contexto existente com novos dados
        ctx.update({
            # Adiciona a variável 'page_title' 
            # para que ela possa ser exibida no template
            'page_title': page_title,
        })
        
        # Retorna o dicionário de contexto finalizado para a renderização
        return ctx

# Exemplo de Function Based View
# def category(request, slug):
#     # Busca no banco de dados apenas os posts publicados 
#     # que pertencem à categoria com o 'slug' recebido
#     posts = Post.objects.get_published()\
#         .filter(category__slug=slug)

#     # Configura a paginação para a lista de posts da categoria
#     paginator = Paginator(posts, PER_PAGE)
    
#     # Pega o número da página atual através dos parâmetros da URL
#     page_number = request.GET.get("page")
    
#     # Recupera os posts específicos daquela página da categoria
#     page_obj = paginator.get_page(page_number)

#     # Verifica se a lista de objetos da página atual está vazia.
#     # Caso não haja nenhum item, interrompe a execução e retorna um 
#     # erro 404 (Página Não Encontrada).
#     if len(page_obj) == 0:
#         raise Http404()

#     # Define o título dinâmico da página utilizando o nome da categoria 
#     # do primeiro item encontrado, seguido por um texto padrão.
#     page_title = f'{page_obj[0].category.name} - Categoria - '

#     # Renderiza o mesmo template 'index.html', 
#     # reaproveitando a estrutura visual para exibir os posts filtrados
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


# Exemplo de Function Based View
# # View responsável por listar os posts filtrados por uma tag específica
# def tag(request, slug):
#     # Busca apenas os posts publicados que contenham a tag com o 'slug' 
#     # recebido na URL
#     posts = Post.objects.get_published()\
#         .filter(tags__slug=slug)

#     # Configura a paginação dividindo a lista de posts 
#     # com base na constante PER_PAGE
#     paginator = Paginator(posts, PER_PAGE)
    
#     # Obtém o número da página atual 
#     # a partir dos parâmetros da URL (ex: ?page=2)
#     page_number = request.GET.get("page")
    
#     # Retorna o objeto da página correspondente 
#     # (trata automaticamente páginas inválidas ou fora de alcance)
#     page_obj = paginator.get_page(page_number)

#     # Verifica se a lista de objetos da página atual está vazia.
#     # Caso não haja nenhum item, interrompe a execução e 
#     # retorna um erro 404 (Página Não Encontrada).
#     if len(page_obj) == 0:
#         raise Http404()

# Define uma View baseada em classe (CBV) personalizada que 
# herda de PostListView para exibir posts filtrados por tags
class TagListView(PostListView):
    # Atributo do Django que define que a view deve retornar 
    # um erro 404 (Http404) caso a lista de objetos venha vazia
    allow_empty = False

    # Sobrescreve o método do Django responsável por 
    # retornar o conjunto de consultas (QuerySet) base dos objetos
    def get_queryset(self) -> QuerySet[Any]:
        # Obtém o QuerySet padrão da classe pai e aplica um filtro 
        # para trazer apenas os posts cuja tag corresponda ao slug recebido na URL
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    # Sobrescreve o método do Django responsável por 
    # enviar dados (contexto) para o template HTML
    def get_context_data(self, **kwargs):
        # Obtém o dicionário de contexto padrão gerado pela classe pai
        ctx = super().get_context_data(**kwargs)
        
        # Monta uma string customizada para o título da página utilizando 
        # o nome da primeira tag associada ao primeiro objeto post da lista
        page_title = (
            f'{self.object_list[0].tags.first().name}'  # type: ignore
            ' - Tag - '
        )
        
        # Atualiza o dicionário de contexto existente com novos dados
        ctx.update({
             # Adiciona a variável 'page_title' 
             # para que ela possa ser exibida no template
            'page_title': page_title,    
        })
        
        # Retorna o dicionário de contexto finalizado para a renderização
        return ctx

# Define a view responsável por processar as buscas de posts no blog
def search(request):
    # Captura o termo de busca enviado via parâmetros 
    # GET na URL (ex: ?search=python) 
    # e remove espaços extras no início e no fim
    search_value = request.GET.get('search', '').strip()

    # Busca no banco de dados apenas os posts publicados 
    # que correspondem ao termo pesquisado
    posts = (
        Post.objects.get_published()
        .filter(
            # Utiliza a classe Q para buscar o termo simultaneamente 
            # no título, no resumo ou no conteúdo completo do post (condição OU)
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]  # Limita a quantidade de resultados exibidos por 
                      # página de acordo com a constante
    )

    page_title = f'{search_value[:30]} - Search - '

    # Renderiza o template HTML padrão de listagem, 
    # enviando os posts encontrados e o valor da busca para o contexto
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )

# O argumento 'request' (requisição) é obrigatório em todas as views.
# Ele carrega os metadados da navegação do usuário 
# (cookies, dados de formulários, se está logado, etc.).
def page(request, slug):
    # Realiza uma consulta (QuerySet) no banco de dados 
    # através do Model Page
    page_obj = (
        Page.objects
        # Filtra apenas as páginas que estão publicadas (True)
        .filter(is_published=True)
        # Filtra o registro cujo campo 'slug' corresponde 
        # ao slug recebido na variável
        .filter(slug=slug)
        # Retorna o primeiro resultado encontrado 
        # (ou None se nenhum registro corresponder aos filtros)
        .first()
    )

    # Verifica se o objeto da página (page_obj) é nulo ou não foi encontrado.
    # Caso seja None, interrompe a execução e retorna um erro 404 
    # (Página Não Encontrada).
    if page_obj is None:
        raise Http404()

    # Define o título dinâmico da página utilizando 
    # o título do próprio objeto, seguido por um texto padrão.
    page_title = f'{page_obj.title} - Página - '

    # O return é obrigatório 
    # porque o Django espera uma resposta (HttpResponse).
    # A função render() processa o arquivo HTML e 
    # o transforma nessa resposta.
    return render(
        # Passa a requisição adiante (obrigatório pelo render)
        request,    
        # O caminho do template que o Django deve renderizar              
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }    
    )


def post(request, slug):
    """
    Esta é uma função de visualização (view) do Django.
    Ela recebe a requisição do usuário ('request') e o 'slug' 
    (a parte amigável da URL que identifica o post, ex: 'meu-primeiro-post').
    """

    # Busca o post no banco de dados
    post_obj = (
        # Utiliza um gerenciador personalizado (Manager) para garantir 
        # que apenas posts com o status "publicado" sejam considerados.
        Post.objects.get_published()
        
        # Filtra a busca para encontrar o post que tenha exatamente 
        # o 'slug' recebido na URL.
        .filter(slug=slug)
        
        # Retorna o primeiro resultado encontrado ou 'None' caso 
        # nenhum post com esse slug seja localizado.
        .first()
    )

    # Verifica se o objeto do post (post_obj) 
    # é nulo ou não foi encontrado no banco de dados.
    # Caso seja None, interrompe a execução e 
    # retorna um erro 404 (Página Não Encontrada).
    if post_obj is None:
        raise Http404()

    # Define o título dinâmico da página utilizando o título do próprio post, 
    # seguido por um texto padrão.
    page_title = f'{post_obj.title} - Post - '

    # Renderiza e retorna a página HTML
    return render(
        # Passa a requisição original obrigatoriamente
        request,       
        # O caminho do template HTML que vai exibir a página               
        'blog/pages/post.html',       
        {
            # O "contexto": um dicionário que envia dados do Python para o HTML.
            # Aqui, a variável 'post' (encontrada acima) 
            # fica disponível no template.
            'post': post_obj,
            'page_title': page_title,
        }
    )
