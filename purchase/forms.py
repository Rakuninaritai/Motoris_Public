from django import forms
from .models import month_choises,year_choises,Purchase_car

class Payment_method(forms.ModelForm):
    # modelsは指定しない
    models=None
    ketu_month=forms.ChoiceField(choices=month_choises,label="有効期限(月)")
    ketu_year=forms.ChoiceField(choices=year_choises,label="有効期限(年)")
    class Meta:
      model=Purchase_car
      fields=['card_number','ketu_month','ketu_year','sec_code','card_meinin']
      labels={
        "card_number":"カード番号","sec_code":"セキュリティコード","card_meinin":"カード名義人"
      }
      widgets = {
            'card_number': forms.TextInput(attrs={
                'placeholder': '1234 1234 1234 1234',
                'pattern': '[0-9 ]{14,16}',
                'title': '14〜16桁の番号を入力してください',
            }),
            'sec_code': forms.TextInput(attrs={
                'placeholder': '123',
                'pattern': '[0-9]{3,4}',
                'title': '3〜4桁の番号を入力してください',
            }),
            'card_meinin': forms.TextInput(attrs={
                'placeholder': 'shuto yamamoto',
            }),
        }

class Purchase_after(forms.Form):
    im=forms.ImageField()