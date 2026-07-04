# Importa o módulo 'string' do Python para ter acesso fácil a 
# sequências de caracteres (como o alfabeto e números).
import string
# Importa SystemRandom, que gera números aleatórios baseados em 
# fontes fornecidas pelo sistema operacional.
# É muito mais seguro e imprevisível do que o 'random' padrão (útil para 
# segurança e URLs únicas).
from random import SystemRandom

# Importa a função utilitária do Django que transforma 
# qualquer texto em uma string amigável para URLs.
# Exemplo: "Olá Mundo!" vira "ola-mundo".
from django.utils.text import slugify


# Função que gera uma sequência aleatória de letras e números 
# com tamanho padrão de 5 caracteres.
def random_letters(k=5):
    # SystemRandom().choices() escolhe caracteres aleatórios da lista fornecida.
    # string.ascii_lowercase puxa letras minúsculas (a-z) e 
    # string.digits puxa números (0-9).
    # O ''.join() junta essa lista de caracteres sorteados 
    # em uma única string de texto.
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits,
        k=k
    ))


# Função que cria um "slug" (texto de URL) estendido com um sufixo aleatório 
# para garantir que ele seja único.
def slugify_new(text, k=5):
    # Transforma o texto original em slug e concatena com um hífen '-' 
    # seguido do texto aleatório gerado acima.
    # Exemplo: se o título do post for "Meu Primeiro Post", o retorno será 
    # algo como "meu-primeiro-post-a8f3g".
    return slugify(text) + '-' + random_letters(k)
