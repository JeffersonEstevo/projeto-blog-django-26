#!/bin/sh
# O "Shebang" acima indica ao sistema que este script deve ser executado usando o interpretador do Shell (/bin/sh).

# O shell irá encerrar a execução do script imediatamente se qualquer comando falhar (retornar um código de erro diferente de 0).
# Isso evita que o Django tente rodar se o banco de dados falhar ou se as migrações quebrarem.
set -e

# Chama o arquivo /scripts/wait_psql.sh
wait_psql.sh
# Chama o arquivo /scripts/collectstatic.sh
collectstatic.sh
# Chama o arquivo /scripts/migrate.sh
migrate.sh
# Chama o arquivo /scripts/runserver.sh
runserver.sh