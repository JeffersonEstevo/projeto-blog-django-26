from django.shortcuts import render

# Define a função da view chamada 'index', que recebe os dados da requisição do usuário através do argumento 'request'
def index(request):    
    # Retorna a renderização final do HTML, combinando a requisição atual com o arquivo de template específico
    return render(        
        # Passa o objeto 'request' obrigatório, que carrega metadados da sessão, navegador e usuário
        request,        
        # Especifica o caminho exato do arquivo HTML que será desenhado na tela do usuário
        'blog/pages/index.html'
    )
