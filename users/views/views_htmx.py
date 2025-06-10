from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from users.forms import UserCreationExtendedForm
from users.models import PerfilUsuario

# Exibir o formulário inline para novo usuário (linha da tabela)
def novo_usuario_inline(request):
    form = UserCreationExtendedForm()
    return render(request, 'users/partials/form_novo_usuario_inline.html', {'form': form})

# Processar criação do usuário via POST (formulário inline)
def criar_usuario(request):
    if request.method == 'POST':
        form = UserCreationExtendedForm(request.POST)
        if form.is_valid():
            # Criar usuário sem salvar para setar senha
            user = form.save(commit=False)
            user.set_password("123456")  # senha padrão fixa
            user.save()

            # Criar perfil associado ao usuário
            PerfilUsuario.objects.create(
                usuario=user,
                nome_completo=form.cleaned_data['nome_completo'],
                telefone=form.cleaned_data.get('telefone', ''),
                hospital=form.cleaned_data.get('hospital'),
                role=form.cleaned_data['role'],
                cargo=form.cleaned_data['cargo'],
            )

            linha_html = render_to_string('users/partials/linha_usuario.html', {'usuario': user}, request=request)

            return HttpResponse(linha_html)
        else:
            form_html = render_to_string('users/partials/form_novo_usuario_inline.html', {'form': form}, request=request)
            return HttpResponse(form_html, status=400)
    else:
        return HttpResponse(status=405)  # Método não permitido

# Listar usuários para preencher a tabela (chamada HTMX)
def listar_usuarios(request):
    usuarios = User.objects.filter(perfilusuario__isnull=False).select_related('perfilusuario', 'perfilusuario__hospital')
    return render(request, 'users/partials/lista_usuarios.html', {'usuarios': usuarios})

# Página principal que exibe a tabela com botão para criar usuário inline
def pagina_usuarios(request):
    return render(request, 'users/cadastro.html')
