# Importa o modelo (tabela do banco de dados) chamado 'SiteSetup' 
# para que possamos buscar as configurações salvas no painel administrativo.
from site_setup.models import SiteSetup


def context_processor_example(request):
    """
    Este é um context processor de exemplo.
    Ele serve apenas para demonstrar como passar uma string simples 
    para os templates.
    """
    # Retorna um dicionário. A chave 'example' vira uma variável no HTML: {{ example }}
    return {
        'example': 'Veio do context processor (example)'
    }


def site_setup(request):
    """
    Este context processor busca dinamicamente as configurações do site 
    (como título, logo, descrição) e as disponibiliza globalmente.
    """
    # Busca no banco de dados todos os objetos de 'SiteSetup'.
    # .order_by('-id') ordena os resultados pelo ID de forma decrescente (do mais novo para o mais antigo).
    # .first() pega apenas o primeiro registro dessa lista (ou seja, a configuração mais recente).
    setup = SiteSetup.objects.order_by('-id').first()

    # Retorna o objeto encontrado dentro de um dicionário.
    # Agora, em qualquer arquivo HTML, você pode usar {{ site_setup.nome_do_campo }}
    return {
        'site_setup': setup,
    }
