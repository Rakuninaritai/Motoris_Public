# shohin/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'guest_name']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'コメントを入力してください'}),
            'guest_name': forms.TextInput(attrs={'placeholder': '名前（任意）'}),
        }