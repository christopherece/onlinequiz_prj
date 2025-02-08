from django.urls import path
from .views import quiz_view, save_drawing

urlpatterns = [
    path('', quiz_view, name='quiz'),
    path('save-drawing/', save_drawing, name='save_drawing'),

]
