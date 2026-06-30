from django.contrib import admin
from site_setup.models import MenuLink

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
