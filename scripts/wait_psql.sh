#!/bin/sh
# Um laço "while" (enquanto). O "nc -z" (Netcat) tenta abrir uma conexão TCP com o banco de dados (usando as variáveis de ambiente do host e porta).
# O "!" inverte a lógica: "Enquanto NÃO conseguir conectar no Postgres, faça..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  # Exibe uma mensagem amarela no terminal do Docker avisando que o banco ainda não está pronto.
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..." 
  
  # Pausa a execução por 2 segundos antes de tentar a conexão novamente, evitando sobrecarregar o processador.
  sleep 2
done

# Mensagem exibida no terminal quando o laço 'while' terminar, indicando que o Postgres aceitou a conexão.
echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"