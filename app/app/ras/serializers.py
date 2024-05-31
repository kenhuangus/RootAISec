from rest_framework import serializers
from . import models
from .contract import reward_tokens
import os


class AuditSerializer(serializers.Serializer):
    wallet = serializers.CharField(source='user.wallet.address')
    file = serializers.FileField()
    score = serializers.FloatField(read_only=True)
    tx_hash = serializers.CharField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        address = validated_data['user']['wallet']['address']
        wallet = models.Wallet.objects.get_or_create(address=address, defaults={
            'address': address
        })[0]
        upload = models.AuditUpload.objects.create(file=validated_data['file'], user=wallet.user)
        upload.calculate_score()
        try:
            upload.reward_tokens()
        except Exception as e:
            print(e)
        return upload


class ContractSerializer(serializers.ModelSerializer):
    wallet = serializers.CharField(source='user.wallet.address')
    file = serializers.FileField()
    score = serializers.FloatField(read_only=True)

    class Meta:
        model = models.ContractUpload
        fields = '__all__'
        read_only_fields = ('user', 'score')

    def create(self, validated_data):
        address = validated_data['user']['wallet']['address']
        wallet = models.Wallet.objects.get_or_create(address=address, defaults={
            'address': address
        })[0]   
        upload = models.ContractUpload.objects.create(file=validated_data['file'], user=wallet.user)
        upload.calculate_score()
        return upload