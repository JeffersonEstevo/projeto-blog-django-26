# É necessário importar a função render, que é um atalho do Django para 
# juntar um arquivo HTML (template) com os dados do banco de dados e 
# entregar ao navegador.
from django.shortcuts import render

# Importa o modelo (tabela) 'Post' do app 'blog' 
# para poder consultar os dados do banco
from blog.models import Post

# Importa a classe do Django responsável por 
# gerenciar a divisão de dados em páginas
from django.core.paginator import Paginator

# Define uma constante com o número máximo de posts 
# que serão exibidos em cada página
PER_PAGE = 9

# Define a função da view chamada 'index', que 
# recebe os dados da requisição do usuário através do argumento 'request'
def index(request): 
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
        }
    )


def created_by(request, author_pk):
    # Busca no banco de dados apenas os posts publicados 
    # que pertencem ao autor com o ID (pk) recebido
    posts = Post.objects.get_published()\
        .filter(created_by__pk=author_pk)

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

    # Renderiza o mesmo template 'index.html', 
    # reaproveitando a estrutura visual para exibir os posts filtrados
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

# View responsável por listar os posts filtrados por uma tag específica
def tag(request, slug):
    # Busca apenas os posts publicados que contenham a tag com o 'slug' recebido na URL
    posts = Post.objects.get_published()\
        .filter(tags__slug=slug)

    # Configura a paginação dividindo a lista de posts com base na constante PER_PAGE
    paginator = Paginator(posts, PER_PAGE)
    
    # Obtém o número da página atual a partir dos parâmetros da URL (ex: ?page=2)
    page_number = request.GET.get("page")
    
    # Retorna o objeto da página correspondente (trata automaticamente páginas inválidas ou fora de alcance)
    page_obj = paginator.get_page(page_number)

    # Renderiza o template do blog passando os posts paginados no contexto
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

# O argumento 'request' (requisição) é obrigatório em todas as views.
# Ele carrega os metadados da navegação do usuário 
# (cookies, dados de formulários, se está logado, etc.).
def page(request, slug):
    # O return é obrigatório 
    # porque o Django espera uma resposta (HttpResponse).
    # A função render() processa o arquivo HTML e 
    # o transforma nessa resposta.
    return render(
        # Passa a requisição adiante (obrigatório pelo render)
        request,    
        # O caminho do template que o Django deve renderizar              
        'blog/pages/page.html'    
    )


def post(request, slug):
    """
    Esta é uma função de visualização (view) do Django.
    Ela recebe a requisição do usuário ('request') e o 'slug' 
    (a parte amigável da URL que identifica o post, ex: 'meu-primeiro-post').
    """

    # Busca o post no banco de dados
    post = (
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
            'post': post,
        }
    )
