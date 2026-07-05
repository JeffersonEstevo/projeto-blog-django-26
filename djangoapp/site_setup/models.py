from django.db import models
# Importa uma função personalizada para redimensionar imagens
from utils.images import resize_image
# Importa um validador personalizado para garantir que o arquivo seja um PNG
from utils.model_validators import validate_png

# Define a classe MenuLink, que representa uma tabela no banco de dados.
# Ela herda de models.Model, transformando esta classe em um modelo do Django.
class MenuLink(models.Model):
    
    # A classe Meta é usada para configurar metadados do modelo 
    # (opções que não são campos).
    class Meta:
        # Define o nome de exibição do modelo no singular (ex: no painel admin).
        verbose_name = 'Menu Link'
        
        # Define o nome de exibição do modelo no plural 
        # (evita que o Django apenas adicione um 's' genérico).
        verbose_name_plural = 'Menu Links'

    # Campo de texto curto (máximo 50 caracteres) 
    # para o texto/nome que aparece no menu.
    text = models.CharField(max_length=50)
    
    # Campo de texto longo (máximo 2048 caracteres) 
    # para armazenar o endereço URL 
    # ou caminho interno do link.
    url_or_path = models.CharField(max_length=2048)
    
    # Campo booleano (verdadeiro/falso). Indica se o link 
    # deve abrir em uma nova aba (target="_blank").
    # Por padrão (default=False), ele abrirá na mesma aba.
    new_tab = models.BooleanField(default=False)

    site_setup = models.ForeignKey(
        # Relaciona este model com o model 'SiteSetup' 
        # (pode ser uma string se o model estiver no mesmo 
        # arquivo ou para evitar importação circular)
        'SiteSetup', 
        # Se o objeto 'SiteSetup' relacionado for deletado, 
        # este registro também será deletado automaticamente (Cascata)
        on_delete=models.CASCADE, 

        # Permite que o campo fique vazio na validação de formulários 
        # (no painel do Django Admin, por exemplo)
        blank=True, 
        # Permite que o banco de dados armazene o valor como NULL 
        # caso não haja relacionamento selecionado
        null=True, 
        # Define que o valor padrão inicial deste campo 
        # para novos registros será None (NULL)
        # Sem o related_name, o Django usa o padrão dele para a relação reversa.
        # Se este campo estiver no modelo 'MenuLink' apontando para 'SiteSetup', 
        # para buscar os links de um site você era obrigado a usar: 
        # site_setup.menulink_set.all()
        # Ao adicionar o related_name='menu', 
        # você batiza a relação reversa com um nome personalizado.
        # Agora, o Django ignora o sufixo padrão '_set' e permite que você acesse 
        # todos os links vinculados a este SiteSetup usando apenas: 
        # site_setup.menu.all()
        default=None, related_name='menu'
    )

    # Método mágico __str__ define a representação em texto deste objeto.
    # Quando o Django precisar exibir esse link 
    # (como na listagem do admin ou em selects), 
    # ele mostrará o conteúdo do campo 'text'.
    def __str__(self):
        return self.text


# Define a classe SiteSetup, 
# que funcionará como a tabela de configurações gerais do seu site.
class SiteSetup(models.Model):
    
    # A classe Meta define metadados e 
    # configurações visuais do modelo no Django.
    class Meta:
        # Define o nome do modelo no singular 
        # dentro do painel de administração.
        verbose_name = 'Setup'
        
        # Define o nome no plural. 
        # Como é uma tela de configuração única (Singleton), 
        # faz sentido manter o plural igual ao singular 
        # para não exibir "Setups".
        verbose_name_plural = 'Setup'

    # Campo de texto curto (máximo 65 caracteres) 
    # para armazenar o título principal do site/blog.
    title = models.CharField(max_length=65)
    
    # Campo de texto (máximo 255 caracteres) 
    # para armazenar uma descrição ou slogan do site.
    description = models.CharField(max_length=255)

    # Chaves booleanas (True/False) 
    # para controlar dinamicamente a exibição de elementos no Front-end:
    
    # Define se o cabeçalho (header) 
    # deve ser exibido na tela. Padrão: Sim (True).
    show_header = models.BooleanField(default=True)
    
    # Define se a barra de pesquisa deve ser exibida. 
    # Padrão: Sim (True).
    show_search = models.BooleanField(default=True)
    
    # Define se o menu de navegação deve ser exibido. 
    # Padrão: Sim (True).
    show_menu = models.BooleanField(default=True)
    
    # Define se o texto de descrição/slogan deve aparecer no layout. 
    # Padrão: Sim (True).
    show_description = models.BooleanField(default=True)
    
    # Define se os botões de paginação (Avançar/Voltar páginas) 
    # devem aparecer. Padrão: Sim (True).
    show_pagination = models.BooleanField(default=True)
    
    # Define se o rodapé (footer) do site deve ser exibido. 
    # Padrão: Sim (True).
    show_footer = models.BooleanField(default=True)

    # Define o campo para upload do favicon do site
    favicon = models.ImageField(
        # Organiza os arquivos em pastas por ano (%Y) e mês (%m) 
        # dentro de 'assets/favicon/'
        upload_to='assets/favicon/%Y/%m/',
        
        # Permite que o campo fique vazio no formulário do admin e 
        # define uma string vazia como padrão caso não haja imagem
        blank=True, default='',
        # Aplica a validação customizada para aceitar 
        # apenas arquivos PNG no upload
        validators=[validate_png],
    )

    # Método mágico que define como o 
    # objeto será representado em formato de texto.
    # Quando o Django precisar listar essa configuração, 
    # ele mostrará o valor salvo no campo 'title'.
    def __str__(self):
        return self.title
    
   # Sobrescrita do método save: altera o comportamento padrão do Django 
   # ao salvar o objeto
    def save(self, *args, **kwargs):
        # Guarda o nome/caminho atual do arquivo de favicon 
        # antes de salvar (convertido para string)
        current_favicon_name = str(self.favicon.name)
        
        # Executa o método save original da classe pai (models.Model), 
        # salvando os dados no banco de dados
        super().save(*args, **kwargs)
        
        # Inicializa uma variável de controle para checar se o favicon mudou
        favicon_changed = False

        # Se existir um arquivo de favicon associado a este objeto...
        if self.favicon:
            # ...verifica se o nome gravado antes do save é diferente 
            # do nome atual (detecta se houve novo upload)
            favicon_changed = current_favicon_name != self.favicon.name

        # Se um novo favicon foi enviado ou modificado...
        if favicon_changed:
            # ...chama a função para redimensionar a imagem do favicon para 
            # o tamanho padrão de 32x32 pixels
            resize_image(self.favicon, 32) 
            