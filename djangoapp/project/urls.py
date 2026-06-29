"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# Importa a função 'include' do Django, 
# usada para conectar as rotas de outros aplicativos 
# ao arquivo de rotas principal
from django.urls import path, include

# Importa o objeto 'settings', que dá acesso a todas as configurações do seu projeto (definidas em settings.py)
from django.conf import settings

# Importa a função helper 'static', que auxilia na criação de rotas para servir arquivos estáticos/mídia
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
]

# Verifica se o modo de depuração (DEBUG) está ativado no seu settings.py.
# Isso é crucial porque o Django NÃO é eficiente (e nem seguro) servindo arquivos de mídia em produção.
if settings.DEBUG:
    
    # Concatena (adiciona) uma nova rota à sua lista existente de 'urlpatterns'
    urlpatterns += static(
        # O primeiro argumento é a URL base que o usuário vai acessar no navegador (ex: '/media/')
        settings.MEDIA_URL,
        
        # O segundo argumento indica o caminho físico no seu computador/servidor onde esses arquivos estão salvos
        document_root=settings.MEDIA_ROOT
    )
