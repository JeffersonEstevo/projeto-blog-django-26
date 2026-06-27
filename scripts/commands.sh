#!/bin/sh
# O "Shebang" acima indica ao sistema que este script deve ser executado usando o interpretador do Shell (/bin/sh).

# O shell irá encerrar a execução do script imediatamente se qualquer comando falhar (retornar um código de erro diferente de 0).
# Isso evita que o Django tente rodar se o banco de dados falhar ou se as migrações quebrarem.
set -e

# Um laço "while" (enquanto). O "nc -z" (Netcat) tenta abrir uma conexão TCP com o banco de dados (usando as variáveis de ambiente do host e porta).
# O "!" inverte a lógica: "Enquanto NÃO conseguir conectar no Postgres, faça..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  # Exibe uma mensagem amarela no terminal do Docker avisando que o banco ainda não está pronto.
  # O "&" no final envia o comando para o background, permitindo que o script continue sem travar.
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..." &
  
  # Pausa a execução por 0.1 segundos antes de tentar a conexão novamente, evitando sobrecarregar o processador.
  sleep 0.1
done

# Mensagem exibida no terminal quando o laço 'while' terminar, indicando que o Postgres aceitou a conexão.
echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Coleta todos os arquivos estáticos do Django (CSS, JS, Imagens) e os agrupa no diretório configurado em STATIC_ROOT.
python manage.py collectstatic --noinput

# Aplica as migrações do banco de dados (cria/atualiza as tabelas de acordo com seus models do Django).
python manage.py migrate

# Inicia o servidor de desenvolvimento nativo do Django para começar a receber requisições.
python manage.py runserver 0.0.0.0:8000