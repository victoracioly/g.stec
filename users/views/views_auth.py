from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from users.forms import UserCreationExtendedForm
from users.models import PerfilUsuario
from django.views.decorators.csrf import csrf_protect

# View de Cadastro
def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationExtendedForm(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(
                usuario=user,
                cargo=form.cleaned_data['cargo'],
                role=form.cleaned_data['role'],
                hospital=form.cleaned_data['hospital']
            )
            login(request, user)
            return redirect('redirecionar_dashboard')
    else:
        form = UserCreationExtendedForm()
    return render(request, 'users/cadastro.html', {'form': form})

# View de Login
@csrf_protect
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(resolve_url('redirecionar_dashboard'))
        messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
