from django.shortcuts import render
from django.http import JsonResponse
import base64
import os
from django.conf import settings
from .models import MathQuestion
import json


def quiz_view(request):
    question = MathQuestion.objects.first()
    return render(request, 'quiz.html', {'question': question})

def save_drawing(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            image_data = data.get('image')

            if not image_data:
                return JsonResponse({'error': 'No image data received'}, status=400)

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f'drawing.{ext}'
            filepath = os.path.join(settings.MEDIA_ROOT, filename)

            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(imgstr))

            file_url = f"{settings.MEDIA_URL}{filename}"
            return JsonResponse({'message': 'Drawing saved successfully!', 'file': filename, 'file_url': file_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)