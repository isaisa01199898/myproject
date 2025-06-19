from django.urls import path
from .views import IndexView, PageCreateView

app_name = 'diary'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('prompt/', PageCreateView.as_view(), name='prompt'),
]
