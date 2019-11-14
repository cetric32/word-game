from django.urls import path

app_name = 'words'

from . import views

urlpatterns = [
    path('letters/',views.letters,name='letters'),
    path('word/validate/', views.validate_word,name='validate_word'),
    path('word/process/<str:word>',views.process_word,name='processword'),
]