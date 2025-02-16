from django.shortcuts import render
from django.http import JsonResponse
import base64
import os
from django.conf import settings
from .models import MathQuestion
import json
from datetime import datetime
import uuid
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage





@login_required(login_url='login')
def quiz_view(request):
    # Fetch the first question from the database
    question = MathQuestion.objects.first()
    # Get the PDF URL for the original PDF
    pdf_url = question.question_pdf.url if question and question.question_pdf else None
    return render(request, 'quiz.html', {'question': question, 'pdf_url': pdf_url})

def save_drawing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            if not image_data:
                return JsonResponse({'error': 'No image data received'}, status=400)
            
            # Get User and Date
            user = request.user.username
            date_str = datetime.now().strftime('%Y-%m-%d')
            parent_email = request.user.email


            # Decode the base64 image data
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]  # Extract the extension (png/jpg)
            filename = f'{user}_drawing_{date_str}.{ext}'  # Unique filename with date

            # Save the image to the media directory
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(imgstr))

             # Convert to Django file for email attachment
            drawing_file = ContentFile(base64.b64decode(imgstr), name=filename)

            # Send email with attachment
            email = EmailMessage(
                subject='Exam has been submitted',
                body=f'{user} has submitted the exam.',
                from_email='balaydalakay@gmail.com',
                to=[parent_email, 'christopheranchetaece@gmail.com'],
            )
            email.attach(filename, drawing_file.read(), f'image/{ext}')
            email.send()

            return JsonResponse({'message': 'Exam saved successfully!', 'file': filename})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
