from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth

def login(request):
    if request.method =="GET":
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet/')
        return render(request, 'login.html')
    
    if request.method =="POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        if len(nome.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.WARNING, 'Preencha todos os campos em branco.')
            return redirect('/auth/cadastro/')
        
        usuario = auth.authenticate(request, username = nome, password = senha)

        if usuario:
            auth.login(request, usuario)
            return redirect('/divulgar/novo_pet/')
        
        else:
            messages.add_message(request, constants.WARNING, 'Credenciais inválidas.')
            return redirect('/auth/cadastro/')  
    



def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet/')
        return render(request, 'cadastro.html')
    
    if request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.WARNING, 'Preencha todos os campos em branco.')
            return redirect('/auth/cadastro/')
        
        if User.objects.filter(username = nome).exists():
            messages.add_message(request, constants.WARNING, 'Nome de Usuário já existente, tente realizar o login.')
            return redirect('/auth/cadastro/')
        
        if User.objects.filter(email = email).exists():
            messages.add_message(request, constants.WARNING, 'Email já cadastrado, tente realizar o login.')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.WARNING, 'As senhas preenchidas não coincidem.')
            return redirect('/auth/cadastro/')
        
        if len(senha.strip()) < 6:
            messages.add_message(request, constants.WARNING, 'Sua senha deverá ter no minímo 6 caracteres.')
            return redirect('/auth/cadastro/')
        
        try:
            usuario = User.objects.create_user(username=nome, email=email, password=senha)
            usuario.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
            return redirect('/auth/login/')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return redirect('/auth/login/')



def sair(request):
    auth.logout(request)
    return redirect('/auth/login/')