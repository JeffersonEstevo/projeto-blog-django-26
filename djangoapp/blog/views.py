# É necessário importar a função render, que é um atalho do Django para 
# juntar um arquivo HTML (template) com os dados do banco de dados e 
# entregar ao navegador.
from django.shortcuts import render

# Define a função da view chamada 'index', que 
# recebe os dados da requisição do usuário através do argumento 'request'
def index(request):    
    # Retorna a renderização final do HTML, combinando a requisição atual 
    # com o arquivo de template específico
    return render(        
        # Passa o objeto 'request' obrigatório, que 
        # carrega metadados da sessão, navegador e usuário
        request,        
        # Especifica o caminho exato do arquivo HTML que 
        # será desenhado na tela do usuário
        'blog/pages/index.html'
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