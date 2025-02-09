from django.db import models

# Create your models here.
class MathQuestion(models.Model):
    question_pdf = models.FileField(upload_to='media/questions/')
    created_at = models.DateTimeField(auto_now_add=True)