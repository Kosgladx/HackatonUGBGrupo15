from django.contrib import admin
from django.urls import path

from core.views import (
    home,
    painel,
    monitor,
    login_view,
    logout_view,
    entrar_grupo,
    sair_grupo,
    adicionar_integrante,
    remover_integrante
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home),

    path('painel/', painel),

    path('monitor/', monitor),

    path('login/', login_view),

    path('logout/', logout_view),

    path('entrar-grupo/<int:grupo_id>/', entrar_grupo),

    path(
        'sair-grupo/<int:grupo_id>/',
        sair_grupo
    ),

    path(
        'adicionar-integrante/<int:usuario_id>/<int:grupo_id>/', 
        adicionar_integrante
    ),

    path(
        'remover-integrante/<int:usuario_id>/',
        remover_integrante
    ),
]