from django.shortcuts import render, redirect, get_object_or_404
from users.models import Hospital, PerfilUsuario
from users.forms import HospitalForm, VinculoHospitalForm
from django.contrib.auth.models import User

# CRUD Hospitais
def listar_hospitais(request):
    hospitais = Hospital.objects.all()
    return render(request, 'users/lista_hospitais.html', {'hospitais': hospitais})

def criar_hospital(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_hospitais')
    else:
        form = HospitalForm()
    return render(request, 'users/form_hospital.html', {'form': form})

def editar_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('listar_hospitais')
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'users/form_hospital.html', {'form': form})

def excluir_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    return redirect('listar_hospitais')

# Vínculo de usuário com Hospital
def vincular_hospital(request, id):
    hospital = get_object_or_404(Hospital, id=id)
    if request.method == 'POST':
        form = VinculoHospitalForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            role = form.cleaned_data['role']
            cargo = form.cleaned_data['cargo']
            perfil, created = PerfilUsuario.objects.get_or_create(usuario=usuario)
            perfil.hospital = hospital
            perfil.role = role
            perfil.cargo = cargo
            perfil.save()
            return redirect('listar_hospitais')
    else:
        form = VinculoHospitalForm(initial={'hospital': hospital})
    return render(request, 'users/vincular_hospital.html', {'form': form, 'hospital': hospital})
