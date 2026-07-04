# Importa a classe Path da biblioteca nativa pathlib 
# para manipulação inteligente de caminhos de arquivos
from pathlib import Path

# Importa as configurações do Django (necessário 
# para descobrir onde fica o diretório MEDIA_ROOT)
from django.conf import settings
# Importa a biblioteca Pillow (PIL) para tratamento e 
# manipulação de imagens
from PIL import Image


# Define a função de redimensionamento com valores padrão (largura de 800px, 
# otimização ativada e qualidade em 60%)
def resize_image(image_django, new_width=800, optimize=True, quality=60):
    # Monta e resolve o caminho absoluto do arquivo combinando 
    # o MEDIA_ROOT do Django com o nome do arquivo enviado
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()
    
    # Abre a imagem fisicamente usando o Pillow 
    # para que possamos manipulá-la
    image_pillow = Image.open(image_path)
    
    # Desestrutura a tupla obtendo a largura e a altura originais da imagem
    original_width, original_height = image_pillow.size

    # Se a largura original já for menor ou igual à largura desejada, 
    # não há necessidade de redimensionar
    if original_width <= new_width:
        # Fecha o arquivo para liberar a memória do servidor
        image_pillow.close()
        # RETORNO: Retorna None (ou você pode retornar a própria imagem, 
        # veja a nota abaixo)
        #O problema: Quando você executa .close(), 
        # o objeto image_pillow é fechado e limpo da memória. 
        # Se você tentar usar essa variável retornada em outro lugar do código 
        # (como no seu models.py), o Python vai estourar um erro dizendo 
        # que a operação foi feita em um arquivo fechado.
        return 

    # Calcula a nova altura de forma proporcional (regra de três) para manter 
    # o aspect ratio da imagem, arredondando o resultado
    new_height = round(new_width * original_height / original_width)

    # Cria uma nova imagem redimensionada utilizando o algoritmo LANCZOS 
    # (alta qualidade para redução)
    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

    # Sobrescreve o arquivo original salvando a nova imagem com a otimização e 
    # qualidade definidas
    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    # Retorna o objeto da nova imagem processada
    return new_image
