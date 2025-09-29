from django import forms
from django.core.exceptions import ValidationError
import re

#フォームクラス作成
class Contact_Form(forms.Form):
    # labelとフィールドの間にある : を取り除く処理
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
    
    Name = forms.CharField(label="お名前")                    
    Tell = forms.IntegerField(label="電話番号")
    Mail = forms.EmailField(label="メールアドレス")
    Text = forms.CharField(widget=forms.Textarea,label="お問合せ内容")