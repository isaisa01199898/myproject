from django import forms
from .models import Diary

class TestForm(forms.Form):
    user_input = forms.CharField(label='入力', max_length=100)

class PageForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'body', 'diary_date']
