from django.shortcuts import render, redirect
from .models import Usuario, Grupo
from django.contrib.auth import authenticate, login, logout


def home(request):

    grupos = Grupo.objects.all().order_by('numero')

    if request.method == 'POST':

        grupo_id = request.POST.get('grupo')

        grupo = None

        if grupo_id != 'sem_grupo':

            grupo = Grupo.objects.get(id=grupo_id)

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

            username = request.POST.get('matricula'),

            nome = request.POST.get('nome'),

            matricula = request.POST.get('matricula'),

            periodo = request.POST.get('periodo'),

            email = request.POST.get('email'),

            telefone = request.POST.get('telefone'),

            tipo = request.POST.get('tipo'),

            grupo = grupo
        )

        usuario.set_password(
            request.POST.get('senha')
        )

        usuario.save()

        if usuario.tipo == 'monitor':
            return redirect('/monitor')

        return redirect('/painel')

    return render(request, 'index.html', {
        'grupos': grupos
    })


def painel(request):

    usuarios = Usuario.objects.all()

    grupos = Grupo.objects.all().order_by('numero')

    sem_grupo = Usuario.objects.filter(grupo=None)

    monitores = Usuario.objects.filter(tipo='monitor')

    return render(request, 'painel.html', {

        'usuarios': usuarios,

        'grupos': grupos,

        'sem_grupo': sem_grupo,

        'monitores': monitores
    })


def monitor(request):

    usuario = request.user

    grupos = Grupo.objects.all().order_by('numero')

    meus_grupos = usuario.grupos_monitorados.all()

    grupos_sem_monitor = []

    for grupo in grupos:
        if not grupo.monitores.exists():
            grupos_sem_monitor.append(grupo)

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
        'grupos': grupos,  # 👈 importante agora
    })

def login_view(request):

    erro = None

    if request.method == 'POST':

        matricula = request.POST.get('matricula')

        senha = request.POST.get('senha')

        usuario = authenticate(
            request,
            username=matricula,
            password=senha
        )

        if usuario is not None:

            login(request, usuario)

            if usuario.tipo == 'monitor':
                return redirect('/monitor')

            return redirect('/painel')

        else:
            erro = 'Matrícula ou senha inválidas'

    return render(request, 'login.html', {
        'erro': erro
    })

def logout_view(request):

    logout(request)

    return redirect('/login')

def entrar_grupo(request, grupo_id):

    if request.user.is_authenticated:

        grupo = Grupo.objects.get(id=grupo_id)

        possui_monitor = grupo.monitores.exists()

        if not possui_monitor:

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

    usuario.grupo = grupo

    usuario.save()

    return redirect('/monitor')

def remover_integrante(request, usuario_id):

    usuario = Usuario.objects.get(id=usuario_id)

    usuario.grupo = None

    usuario.save()

    return redirect('/monitor')