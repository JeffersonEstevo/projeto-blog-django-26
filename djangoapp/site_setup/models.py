from django.db import models

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

    # Método mágico __str__ define a representação em texto deste objeto.
    # Quando o Django precisar exibir esse link 
    # (como na listagem do admin ou em selects), 
    # ele mostrará o conteúdo do campo 'text'.
    def __str__(self):
        return self.text
    