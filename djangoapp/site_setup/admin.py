from django.contrib import admin
from site_setup.models import MenuLink, SiteSetup

# ANTES: MenuLink tinha sua própria página de administração corporativa (@admin.register(MenuLink))
# AGORA: Ele foi transformado em um Inline para ser editado DIRETAMENTE dentro da página de SiteSetup.
class MenuLinkInline(admin.TabularInline):
    """
    Permite criar, editar ou excluir MenuLinks diretamente na mesma tela 
    de edição do SiteSetup, exibidos em formato de tabela (TabularInline).
    """
    model = MenuLink
    
    # Define quantos formulários em branco para novos links aparecerão por padrão
    extra = 1

# O decorator @admin.register vincula o modelo SiteSetup a 
# esta classe de configuração,
# fazendo com que ele apareça no painel administrativo do Django.
@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    
    # Define que apenas as colunas 
    # 'title' (Título) e 'description' (Descrição) 
    # serão exibidas na tabela de listagem do painel.
    list_display = 'title', 'description',

    # Acopla o Inline do MenuLink aqui. 
    # Agora, ao abrir um SiteSetup, os MenuLinks relacionados aparecerão na mesma página.
    # É boa prática usar uma tupla/lista aqui
    inlines = (MenuLinkInline,)  

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
    