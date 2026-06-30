from django.contrib import admin
from site_setup.models import MenuLink, SiteSetup

# O decorator @admin.register vincula o modelo MenuLink a esta classe de configuração,
# registrando-o para aparecer no painel administrativo do Django.
@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    
    # Define as colunas que serão exibidas na tabela de listagem dos links.
    list_display = 'id', 'text', 'url_or_path',
    
    # Define quais dessas colunas serão clicáveis para abrir a tela de edição do link.
    # Por padrão apenas a primeira é, mas aqui todas viram atalhos para edição.
    list_display_links = 'id', 'text', 'url_or_path',
    
    # Ativa uma barra de pesquisa no topo da página que permite filtrar os
    # resultados buscando por correspondências no ID, no texto ou na URL.
    search_fields = 'id', 'text', 'url_or_path',


# O decorator @admin.register vincula o modelo SiteSetup a 
# esta classe de configuração,
# fazendo com que ele apareça no painel administrativo do Django.
@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    
    # Define que apenas as colunas 
    # 'title' (Título) e 'description' (Descrição) 
    # serão exibidas na tabela de listagem do painel.
    list_display = 'title', 'description',

    # Sobrescreve o método do Django que concede ou nega a permissão de 
    # ADICIONAR um novo registro.
    def has_add_permission(self, request):
        # 'SiteSetup.objects.exists()' verifica se 
        # já existe algum registro no banco de dados.
        # O 'not' inverte o resultado: se já EXISTIR um registro, 
        # ele retorna False (bloqueia o botão de adicionar).
        # Se NÃO EXISTIR nenhum, retorna True 
        # (permite criar a primeira e única configuração).
        return not SiteSetup.objects.exists()
    