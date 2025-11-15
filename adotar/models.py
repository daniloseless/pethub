from django.db import models
from django.contrib.auth.models import User
from divulgar.models import Pet,Raca,Tag


class PedidoAdocao(models.Model):
    choice_status = (('AG','Aguardando Aprovação'),('AP','Aprovado'),('R','Recusado'))
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pet = models.ForeignKey(Pet,on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    status = models.CharField(max_length=2, choices=choice_status, default='AG')

    def __str__(self):
        return self.pet.nome


