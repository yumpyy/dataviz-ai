from django.db import models

class Prompts(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    prompt = models.TextField()
