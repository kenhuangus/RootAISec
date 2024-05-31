from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from . import serializers, models 


# Create your views here.
class AuditViewset(ModelViewSet):
    serializer_class = serializers.AuditSerializer
    queryset = models.AuditUpload.objects.all()


class ContractViewset(ModelViewSet):
    serializer_class = serializers.ContractSerializer
    queryset = models.ContractUpload.objects.all()
    

def index(request):
    return render(request, 'index.html')

