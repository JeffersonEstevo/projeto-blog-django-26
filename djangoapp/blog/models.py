# Importa o módulo models do Django para mapear 
# as classes como tabelas no banco de dados
from django.db import models
# Importa a função utilitária personalizada que 
# cria slugs únicos com sufixo aleatório
from utils.rands import slugify_new

# Define a tabela 'Tag' no banco de dados
class Tag(models.Model):
    # A classe Meta altera configurações internas e comportamentos do modelo
    class Meta:
        # Nome exibido no singular no painel administrativo
        verbose_name = 'Tag'
        # Nome exibido no plural no painel administrativo          
        verbose_name_plural = 'Tags'   

    # Campo de texto curto para armazenar o 
    # nome da Tag (máximo de 255 caracteres)
    name = models.CharField(max_length=255)
    
    # Campo específico para URLs amigáveis (slug).
    # unique=True: impede URLs duplicadas no banco de dados.
    # null=True e blank=True: permite que o campo fique vazio 
    # no formulário e no banco antes de ser gerado.
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    # Sobrescreve o método save padrão do Django, interceptando o momento 
    # em que o objeto é guardado no banco
    def save(self, *args, **kwargs):
        # Se a tag não tiver um slug preenchido 
        # (ou seja, está sendo criada agora sem slug manual)
        if not self.slug:
            # Gera um slug único baseado no nome da tag, 
            # adicionando 4 caracteres aleatórios no final
            self.slug = slugify_new(self.name, 4)
        # Executa o método save original da classe mãe 
        # (models.Model) para efetivar a gravação no banco
        return super().save(*args, **kwargs)

    # Define a representação em texto da Tag.
    # Faz com que ela apareça pelo próprio nome (self.name) no painel admin.
    def __str__(self) -> str:
        return self.name

# Define a tabela 'Category' no banco de dados
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # Campo de texto curto para armazenar o nome da Categoria
    name = models.CharField(max_length=255)
    
    # Campo específico para URLs amigáveis da categoria
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    # Sobrescreve o método save para automatizar a geração do slug da categoria
    def save(self, *args, **kwargs):
        # Se nenhum slug foi enviado manualmente pelo admin
        if not self.slug:
            # Gera o slug automaticamente usando o nome da categoria 
            # com sufixo de 4 caracteres
            self.slug = slugify_new(self.name, 4)
        # Salva as alterações definitivamente no banco de dados
        return super().save(*args, **kwargs)

    # Define a representação em texto da Categoria.
    # Faz com que ela apareça pelo próprio nome (self.name) no painel admin.
    def __str__(self) -> str:
        return self.name

# Define o modelo (tabela no banco de dados) chamado 'Page'
class Page(models.Model):
    # Campo de texto curto para o título da página, com limite de 65 caracteres
    title = models.CharField(max_length=65,)
    
    # Campo para a URL amigável (slug). É único no banco, não pode ser nulo, 
    # aceita ficar em branco no formulário (blank=True) e tem máximo de 255 caracteres
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    
    # Campo do tipo verdadeiro/falso (checkbox). Começa como falso por padrão
    # e exibe um texto de ajuda explicativo no painel de administração
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    
    # Campo de texto longo para o conteúdo principal da página (sem limite de caracteres)
    content = models.TextField()

    # Sobrescreve o método padrão de salvamento do Django
    def save(self, *args, **kwargs):
        # Verifica se o slug está vazio. Se estiver, gera um slug automaticamente 
        # usando uma função personalizada (slugify_new) baseada no título da página
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
            
        # Chama o método save() original da classe mãe (Django) para gravar os dados de fato no banco
        return super().save(*args, **kwargs)

    # Define a representação em texto do modelo 'Page'. 
    # Fará com que a página apareça com o seu próprio 'title' listado no painel admin
    def __str__(self) -> str:
        return self.title
    