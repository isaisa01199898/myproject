from django.urls import path
from . import views
from .views import IndexView

app_name = 'diary'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # URL名を 'index' に設定
    path('prompt/', views.prompt, name='prompt'),
    path('generate/', views.generate_response, name='generate_response'),

]
