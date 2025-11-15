from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Tag, Raca, Pet
from django.contrib.messages import constants
from django.contrib import messages
from adotar.models import PedidoAdocao  
from django.views.decorators.csrf import csrf_exempt


def novo_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        raca = Raca.objects.all()
        return render(request, 'novo_pet.html',{'tags':tags,'raca':raca})
    
    if request.method =="POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')
        foto = request.FILES.get('foto')

        if len(nome.strip()) == 0 or len(estado.strip()) == 0 or len(cidade.strip()) == 0 or len(telefone.strip()) == 0:
            messages.add_message(request,constants.INFO,'Preencha todos os campos.')
            return redirect('/divulgar/novo_pet/')
        
        if not foto:
            messages.add_message(request,constants.INFO,'Envie uma foto, para finalizar o cadastro do Pet!')
            return redirect('/divulgar/novo_pet/')
        
        if not tags:
            messages.add_message(request,constants.INFO,'Selecione ao menos uma tag ao seu Pet!')
            return redirect('/divulgar/novo_pet/')

        pet = Pet( usuario = request.user ,nome = nome, descricao = descricao, estado = estado, cidade = cidade, telefone = telefone, raca_id = raca, foto = foto)
        pet.save()

        for tag_id in tags:
            tag = Tag.objects.get(id = tag_id)
            pet.tags.add(tag)
        
        pet.save()
        messages.add_message(request,constants.INFO,'Novo Pet cadastrado!')
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return redirect('/divulgar/seus_pets/')


def seus_pets(request):
    if request.method =="GET":
        pets = Pet.objects.filter(usuario = request.user)
        return render(request,'seus_pets.html',{'pets':pets})
    

def remover_pet(request, id):
    pet = Pet.objects.get(id = id)
    if pet.usuario == request.user:
        pet.delete()
        messages.add_message(request,constants.SUCCESS,'Pet removido com sucesso!')
        return redirect('/divulgar/seus_pets/')
    
    else:
        messages.add_message(request,constants.ERROR,'Esse Pet não pertence a você.')
        return redirect('/divulgar/seus_pets/')




def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})



def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')
    

@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)