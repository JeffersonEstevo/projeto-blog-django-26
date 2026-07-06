# Importa o módulo models do Django para mapear 
# as classes como tabelas no banco de dados
from django.db import models
# Importa a função utilitária personalizada que 
# cria slugs únicos com sufixo aleatório
from utils.rands import slugify_new
# Importa o modelo padrão de usuários do Django para gerenciar autores e editores
from django.contrib.auth.models import User
# Importa a função utilitária responsável por redimensionar e otimizar imagens
from utils.images import resize_image

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
    # aceita ficar em branco no formulário (blank=True) 
    # e tem máximo de 255 caracteres
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
    
    # Campo de texto longo para o conteúdo principal da página 
    # (sem limite de caracteres)
    content = models.TextField()

    # Sobrescreve o método padrão de salvamento do Django
    def save(self, *args, **kwargs):
        # Verifica se o slug está vazio. Se estiver, 
        # gera um slug automaticamente 
        # usando uma função personalizada (slugify_new) 
        # baseada no título da página
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
            
        # Chama o método save() original da classe mãe (Django) 
        # para gravar os dados de fato no banco
        return super().save(*args, **kwargs)

    # Define a representação em texto do modelo 'Page'. 
    # Fará com que a página apareça com o seu próprio 'title' 
    # listado no painel admin
    def __str__(self) -> str:
        return self.title


# Define o modelo principal 'Post' que representará 
# a tabela de artigos no banco de dados
class Post(models.Model):
    # A classe Meta altera configurações internas e metadados do modelo
    class Meta:
        # Nome do modelo no singular no painel administrativo
        verbose_name = 'Post'          
        # Nome do modelo no plural no painel administrativo
        verbose_name_plural = 'Posts'   

    # Campo de texto curto para o título do post (máximo de 65 caracteres)
    title = models.CharField(max_length=65,)
    
    # Campo para a URL amigável. É único no banco, 
    # obrigatório (null=False), 
    # mas opcional no formulário (blank=True) 
    # para que possa ser gerado automaticamente
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    
    # Um resumo ou linha de apoio para o post (máximo de 150 caracteres)
    excerpt = models.CharField(max_length=150)
    
    # Controle de publicação (checkbox). Falso por padrão, 
    # com texto explicativo no admin
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para o post ser exibido publicamente.'
        ),
    )
    
    # Campo de texto longo para armazenar todo o conteúdo/corpo do post
    content = models.TextField()
    
    # Campo para upload de imagem de capa.
    # Organiza os arquivos em pastas por Ano/Mês (%Y/%m)
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    
    # Controle visual para decidir se a imagem de capa aparece ou não 
    # no corpo da página do post
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Se marcado, exibirá a capa dentro do post.',
    )
    
    # Registra automaticamente a data/hora exata 
    # em que o post foi criado (não muda depois)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relacionamento de Chave Estrangeira (Muitos posts para 1 Usuário) 
    # indicando quem criou o post.
    # Se o usuário dono for deletado, este campo fica como NULL (vazio) 
    # mantendo o post intacto.
    # O 'related_name' permite buscar os posts criados pelo usuário via: 
    # user.post_created_by.all()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    
    # Atualiza automaticamente a data/hora toda vez que 
    # o post for modificado e salvo
    # Nota: No Django padrão usa-se 'auto_now=True'
    updated_at = models.DateTimeField(auto_now=True) 
    
    # Semelhante ao 'created_by', 
    # mas mapeia qual usuário fez a última edição no post.
    # O 'related_name' permite buscar posts editados pelo usuário via: 
    # user.post_updated_by.all()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    
    # Relacionamento Muitos para Um com o modelo Category. 
    # Cada post pertence a uma categoria.
    # Se a categoria for excluída, o post não é deletado (o campo vira NULL)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    
    # Relacionamento Muitos para Muitos (Um post pode ter várias tags, 
    # e uma tag pode estar em vários posts)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    # Define que a representação em formato de texto deste objeto será 
    # o próprio título do post
    def __str__(self):
        return self.title

    # Sobrescreve o método save() para interceptar o salvamento
    def save(self, *args, **kwargs):
        # Se o campo slug estiver vazio no momento de salvar, 
        # gera um slug baseado no título
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
            
        # Guarda o nome atual do arquivo de imagem (da capa) 
        # antes de qualquer alteração ser salva
        current_cover_name = str(self.cover.name)

        # Executa o método save original do Django para 
        # salvar os dados atuais no banco de dados
        super_save = super().save(*args, **kwargs)

        # Inicializa uma variável de controle (flag) 
        # definindo que a capa NÃO mudou por padrão
        cover_changed = False

        # Verifica se o objeto possui um arquivo de capa associado
        if self.cover:
            # Compara o nome antigo (guardado antes) com o nome atual. 
            # Se forem diferentes, significa que o usuário 
            # fez upload de uma nova imagem.
            cover_changed = current_cover_name != self.cover.name

        # Se a imagem foi alterada ou adicionada agora...
        if cover_changed:
            # Redimensiona a nova imagem para a largura de 900px, 
            # ativa o crop/otimização (True) e define a qualidade em 70%
            resize_image(self.cover, 900, True, 70)

        # Retorna o resultado do salvamento padrão que foi executado lá atrás
        return super_save
    