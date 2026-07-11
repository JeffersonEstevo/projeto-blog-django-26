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
    # Cria uma consulta (QuerySet) no banco de dados para buscar os posts
    posts = (
        Post
        .objects # Acessa o gerenciador do banco de dados do modelo Post
        # Filtra para trazer apenas os posts que estão publicados
        .filter(is_published=True) 
        # Ordena os posts de forma decrescente (do mais novo para o mais antigo)
        .order_by('-pk') 
    )

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


# O argumento 'request' (requisição) é obrigatório em todas as views.
# Ele carrega os metadados da navegação do usuário 
# (cookies, dados de formulários, se está logado, etc.).
def page(request):
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


def post(request):
    # Mesma lógica: recebe a requisição de quem acessou a URL do post
    # e renderiza o HTML específico da página de post.
    return render(
        request,
        'blog/pages/post.html'
    )