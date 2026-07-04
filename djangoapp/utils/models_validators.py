# # Importa a exceção de validação padrão do Django, usada para 
# # lançar erros em formulários e no admin
# from django.core.exceptions import ValidationError

# # Define a função de validação que receberá o arquivo de imagem enviado
# def validate_png(image):
#     # Converte o nome do arquivo para letras minúsculas (.lower()) e 
#     # verifica se ele NÃO termina com '.png'
#     if not image.name.lower().endswith('.png'):
#         # Se não for um PNG, interrompe o salvamento e exibe 
#         # a mensagem de erro na tela para o usuário
#         raise ValidationError('Imagem precisa ser PNG.')
    
# Importa a exceção do Django para lançar erros de validação no formulário/admin
from django.core.exceptions import ValidationError
# Importa a classe Image do Pillow para ler os metadados internos do arquivo
from PIL import Image

def validate_png(image):
    # 1. CHECAGEM RÁPIDA: Verifica de forma leve se a extensão do arquivo não é '.png'
    if not image.name.lower().endswith('.png'):
        # Se falhar na extensão, barra o upload imediatamente antes de processar o arquivo
        raise ValidationError('Imagem precisa ser PNG.')
        
    # 2. CHECAGEM REAL: Tenta abrir o arquivo para analisar o cabeçalho binário dele
    try:
        # O 'with' garante que o arquivo da imagem será fechado automaticamente após o teste
        with Image.open(image) as img:
            # Verifica se o formato interno identificado pelo Pillow é diferente de 'PNG'
            if img.format != 'PNG':
                # Pega usuários que renomearam um arquivo .jpg ou .exe para .png de má fé
                raise ValidationError('O arquivo parece um PNG pela extensão, mas não é um PNG válido.')
    # Se o Pillow não conseguir abrir o arquivo (arquivo corrompido, texto puro disfarçado, etc)
    except Exception:
        # Lança um erro genérico avisando que o arquivo está quebrado ou é inválido
        raise ValidationError('Arquivo de imagem corrompido ou inválido.')
