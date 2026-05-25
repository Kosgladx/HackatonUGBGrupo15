from django.shortcuts import render, redirect
from .models import Usuario, Grupo
from django.contrib.auth import authenticate, login, logout


def home(request):

    grupos = Grupo.objects.all().order_by('numero')

    if request.method == 'POST':

        grupo_id = request.POST.get('grupo')

        grupo = None

        # 🔥 CORREÇÃO PRINCIPAL (EVITA CRASH)
        if grupo_id and grupo_id != 'sem_grupo':
            try:
                grupo = Grupo.objects.get(id=grupo_id)
            except Grupo.DoesNotExist:
                grupo = None

            if grupo:
                quantidade = Usuario.objects.filter(
                    grupo=grupo,
                    tipo='integrante'
                ).count()

                if quantidade >= 5:
                    return render(request, 'index.html', {
                        'grupos': grupos,
                        'erro': 'Esse grupo já possui 5 integrantes.'
                    })

        usuario = Usuario(
            username=request.POST.get('matricula'),
            nome=request.POST.get('nome'),
            matricula=request.POST.get('matricula'),
            periodo=request.POST.get('periodo'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            tipo=request.POST.get('tipo'),
            grupo=grupo
        )

        usuario.set_password(request.POST.get('senha'))
        usuario.save()

        if usuario.tipo == 'monitor':
            return redirect('/monitor')

        return redirect('/painel')

    return render(request, 'index.html', {
        'grupos': grupos
    })


def painel(request):

    return render(request, 'painel.html', {
        'usuarios': Usuario.objects.all(),
        'grupos': Grupo.objects.all().order_by('numero'),
        'sem_grupo': Usuario.objects.filter(grupo=None),
        'monitores': Usuario.objects.filter(tipo='monitor')
    })


def monitor(request):

    usuario = request.user
    grupos = Grupo.objects.all().order_by('numero')
    meus_grupos = usuario.grupos_monitorados.all()

    grupos_sem_monitor = [
        g for g in grupos if not g.monitores.exists()
    ]

    integrantes_sem_grupo = Usuario.objects.filter(
        tipo='integrante',
        grupo=None
    ).order_by('nome')

    for grupo in grupos:
        grupo.contagem_integrantes = Usuario.objects.filter(
            grupo=grupo,
            tipo='integrante'
        ).count()

    return render(request, 'monitor.html', {
        'usuario': usuario,
        'meus_grupos': meus_grupos,
        'grupos_sem_monitor': grupos_sem_monitor,
        'integrantes_sem_grupo': integrantes_sem_grupo,
        'grupos': grupos,
    })


def login_view(request):

    erro = None

    if request.method == 'POST':

        usuario = authenticate(
            request,
            username=request.POST.get('matricula'),
            password=request.POST.get('senha')
        )

        if usuario:

            login(request, usuario)

            if usuario.tipo == 'monitor':
                return redirect('/monitor')

            return redirect('/painel')

        erro = 'Matrícula ou senha inválidas'

    return render(request, 'login.html', {'erro': erro})


def logout_view(request):
    logout(request)
    return redirect('/login')


def entrar_grupo(request, grupo_id):

    if request.user.is_authenticated:

        grupo = Grupo.objects.get(id=grupo_id)

        if not grupo.monitores.exists():

            grupo.monitores.add(request.user)
            request.user.tipo = 'monitor'
            request.user.save()

    return redirect('/monitor')


def sair_grupo(request, grupo_id):

    grupo = Grupo.objects.get(id=grupo_id)
    grupo.monitores.remove(request.user)

    return redirect('/monitor')


def adicionar_integrante(request, usuario_id, grupo_id):

    usuario = Usuario.objects.get(id=usuario_id)
    grupo = Grupo.objects.get(id=grupo_id)

    if request.user.tipo != 'monitor':
        return redirect('/monitor')

    qtd = Usuario.objects.filter(
        grupo=grupo,
        tipo='integrante'
    ).count()

    if qtd >= 5:
        return redirect('/monitor')

    usuario.grupo = grupo
    usuario.save()

    return redirect('/monitor')


def remover_integrante(request, usuario_id):

    usuario = Usuario.objects.get(id=usuario_id)
    usuario.grupo = None
    usuario.save()

    return redirect('/monitor')


def salvar_whatsapp(request, grupo_id):

    if request.method == "POST":

        grupo = Grupo.objects.get(id=grupo_id)

        if request.user.tipo != "monitor":
            return redirect("/monitor")

        link = request.POST.get("whatsapp_link")

        grupo.whatsapp_link = link
        grupo.save()

    return redirect("/monitor")