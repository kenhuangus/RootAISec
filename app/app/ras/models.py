from django.db import models
from django.contrib.auth.models import User
from llama_parse import LlamaParse
import os
import json
import nest_asyncio
from pypdf import PdfReader
from vectordb import vectordb
from ollama import Client
from .contract import reward_tokens

def get_pdf_text(filepath):
    reader = PdfReader(filepath)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if self.user is None:
            # Create a new user
            username = 'user{}'.format(User.objects.count() + 1)
            password = User.objects.make_random_password()
            self.user = User.objects.create_user(username=username, password=password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.address


class AuditUpload(models.Model):
    file = models.FileField(upload_to='audits/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name='uploads')
    score = models.FloatField(default=0.0)
    tx_hash = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        # self.tx_hash = reward_tokens(self.user.wallet.address, 100000)
        super().save(*args, **kwargs)

    def get_vectordb_text(self):
        # Do the llama thing
        # parser = LlamaParse() 
        # parser = LlamaParse(result_type='text', verbose=True)
        # document = parser.load_data(self.file.path)
        document = get_pdf_text(self.file.path)
        print(f'Document has {len(document)} characters')
        return document.replace('\x00', '')

    def reward_tokens(self):
        self.tx_hash = reward_tokens(self.user.wallet.address, 100000)
        self.save()

    def calculate_score(self):
        score = 0
        client = Client(host='http://host.docker.internal:11434')
        print('calculating score')
        while not score:
            output = client.generate('rootaisec', format='json', prompt=f'What is the score of the following audit out of 100? Be sure to only respond with the score.')
            output = output['response']
            try:
                output = json.loads(output)
                score = float(output.get('score'))
                break
            except:
                print('unable to get a score')
                pass
        print(output)
        self.score = score
        self.save()

    def get_vectordb_metadata(self):
        return {'title': self.file.name}

    def __str__(self):
        return self.file.name

class ContractUpload(models.Model):
    file = models.FileField(upload_to='contracts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name='audits')
    score = models.FloatField(default=0.0)

    def calculate_score(self):
        score = 0
        client = Client(host='http://host.docker.internal:11434')
        print('calculating score')
        while not score:
            output = client.generate('rootaisec', format='json', prompt=f'What is the score of the following audit out of 100? Be sure to only respond with the score.')
            output = output['response']
            try:
                output = json.loads(output)
                score = float(output.get('score'))
                break
            except:
                print('unable to get a score')
                pass
        print(output)
        self.score = score
        self.save()

    def __str__(self):
        return self.file.name