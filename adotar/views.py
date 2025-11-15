from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import constants
from django.contrib import messages
from divulgar.models import Pet, Raca, Tag
from django.http import HttpResponse
from datetime import datetime
from .models import PedidoAdocao
from django.core.mail import send_mail


def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status='P')
        racas = Raca.objects.all()
        raca_filter = request.GET.get('raca')
        cidade = request.GET.get('cidade')
        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca_id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)
        return render(request, 'listar_pets.html', {'pets': pets, 'racas': racas, 'raca_filter': raca_filter, 'cidade': cidade})


def ver_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    return render(request, 'ver_pet.html', {'pet': pet})


def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status='P')
    pedido = PedidoAdocao(usuario=request.user,
                          pet=pet.first(), data=datetime.now())
    pedido.save()
    messages.add_message(request, constants.SUCCESS,
                         'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    if not pet.exists():
        messages.add_message(request, constants.ERROR,
                             'Esse Pet já foi adotado.')
        return redirect('/adotar/')
    return redirect('/adotar/')


def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(
            usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})


def processa_pedido_adocao(request, id_pedido):
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    pet = Pet.objects.get(id=pedido.pet.id)
    status = request.GET.get('status')
    if status == 'A':
        pedido.status = 'AP'
        string = "Sua adoção foi aprovada com sucesso!"
        pet.status = "A"
    elif status == 'R':
        pedido.status = 'R'
        string = "Infelizmente sua adoção foi recusada..."
    pedido.save()
    pet.save()
    email = send_mail('Sua adoção foi processada',
                      string,
                      'selessdanilob@hotmail.com',
                      [pedido.usuario.email,]
                      )

    messages.add_message(request, constants.SUCCESS,
                         'Pedido de adoção processado com sucesso!')
    return redirect('/divulgar/ver_pedido_adocao')
