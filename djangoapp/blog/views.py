# É necessário importar a função render, que é um atalho do Django para 
# juntar um arquivo HTML (template) com os dados do banco de dados e 
# entregar ao navegador.
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
from django.http import Http404

# Importa a classe do Django responsável por 
# gerenciar a divisão de dados em páginas
from django.core.paginator import Paginator

# Importa a classe Q do Django, permitindo criar consultas complexas 
# com operadores lógicos (como o OU / OR)
from django.db.models import Q

# Define uma constante com o número máximo de posts 
# que serão exibidos em cada página
PER_PAGE = 9

# Define a função da view chamada 'index', que 
# recebe os dados da requisição do usuário através do argumento 'request'
def index(request): 
    # Function Based Views -> São funções
    # Class Based Views -> são classes (POOs)
    # Para mais informações consultar:
    # https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/

    # Chama o gerenciador customizado do modelo Post, 
    # executa o método get_published() 
    # (que filtra os publicados e ordena por ID decrescente) 
    # e armazena o resultado na variável 'posts'.
    posts = Post.objects.get_published()

    # Inicializa o paginador do Django, 
    # passando a lista de posts e a quantidade permitida por página
    paginator = Paginator(posts, PER_PAGE)
    # Captura o número da página atual 
    # a partir dos parâmetros da URL (ex: /?page=2)
    page_number = request.GET.get("page")

    # Busca os posts específicos daquela página 
    # (se 'page' estiver vazio, traz a primeira página)
    page_obj = paginator.get_page(page_number)

    # Renderiza e renderiza a página HTML final para o usuário
    return render(
        request, # A requisição do usuário (obrigatório do Django)
        'blog/pages/index.html', # O caminho do arquivo HTML que será exibido
        {   # Passa os posts da página atual para o HTML conseguir listá-los
            'page_obj': page_obj, 
            # Passa o título da página atual para o HTML conseguir exibir
            'page_title': 'Home - ',
        }
    )


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

    # Define o nome padrão para exibição como sendo o username (nome de usuário).
    user_full_name = user.username

    # Verifica se o usuário possui um primeiro nome cadastrado. 
    # Se tiver, sobrescreve user_full_name combinando o primeiro e o último nome.
    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'
    # Cria o título personalizado da página combinando o nome do autor com um texto padrão.
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


def category(request, slug):
    # Busca no banco de dados apenas os posts publicados 
    # que pertencem à categoria com o 'slug' recebido
    posts = Post.objects.get_published()\
        .filter(category__slug=slug)

    # Configura a paginação para a lista de posts da categoria
    paginator = Paginator(posts, PER_PAGE)
    
    # Pega o número da página atual através dos parâmetros da URL
    page_number = request.GET.get("page")
    
    # Recupera os posts específicos daquela página da categoria
    page_obj = paginator.get_page(page_number)

    # Verifica se a lista de objetos da página atual está vazia.
    # Caso não haja nenhum item, interrompe a execução e retorna um 
    # erro 404 (Página Não Encontrada).
    if len(page_obj) == 0:
        raise Http404()

    # Define o título dinâmico da página utilizando o nome da categoria 
    # do primeiro item encontrado, seguido por um texto padrão.
    page_title = f'{page_obj[0].category.name} - Categoria - '

    # Renderiza o mesmo template 'index.html', 
    # reaproveitando a estrutura visual para exibir os posts filtrados
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

# View responsável por listar os posts filtrados por uma tag específica
def tag(request, slug):
    # Busca apenas os posts publicados que contenham a tag com o 'slug' 
    # recebido na URL
    posts = Post.objects.get_published()\
        .filter(tags__slug=slug)

    # Configura a paginação dividindo a lista de posts 
    # com base na constante PER_PAGE
    paginator = Paginator(posts, PER_PAGE)
    
    # Obtém o número da página atual 
    # a partir dos parâmetros da URL (ex: ?page=2)
    page_number = request.GET.get("page")
    
    # Retorna o objeto da página correspondente 
    # (trata automaticamente páginas inválidas ou fora de alcance)
    page_obj = paginator.get_page(page_number)

    # Verifica se a lista de objetos da página atual está vazia.
    # Caso não haja nenhum item, interrompe a execução e 
    # retorna um erro 404 (Página Não Encontrada).
    if len(page_obj) == 0:
        raise Http404()

    # Define o título dinâmico da página utilizando o nome da primeira tag 
    # associada ao primeiro item, seguido por um texto padrão.
    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    # Renderiza o template do blog passando os posts paginados no contexto
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

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
    # Caso seja None, interrompe a execução e retorna um erro 404 (Página Não Encontrada).
    if page_obj is None:
        raise Http404()

    # Define o título dinâmico da página utilizando o título do próprio objeto, seguido por um texto padrão.
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

    # Verifica se o objeto do post (post_obj) é nulo ou não foi encontrado no banco de dados.
    # Caso seja None, interrompe a execução e retorna um erro 404 (Página Não Encontrada).
    if post_obj is None:
        raise Http404()

    # Define o título dinâmico da página utilizando o título do próprio post, seguido por um texto padrão.
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
