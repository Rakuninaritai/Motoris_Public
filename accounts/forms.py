from django import forms
from .models import Profile
# formはユーザーモデルを取得してして使用することが出来る(modelはdjangoが立ち上がる上がる前から読み込まないといけないから取得できない)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# modelで指定しているuserのsettingsは文字列を返すのに対しこちらは実際のモデルを返すので適している
CustomUser = get_user_model()


#ユーザー登録と、必要な項目
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'aaa@example.com'}),label="メールアドレス")
    
    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']
        labels={"username":"ユーザー名","password1":"パスワード","password2":"パスワード(再度)"}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'りすたろう'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'パスワードを入力'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'パスワードを再入力'}),
        }

# パスワード忘れたとき用のメルアド打ち込み
class PwwsrM(forms.Form):
    email=forms.EmailField(label="ログインしたいアカウントのメールアドレス")
    
# パスワード忘れようのメルアドに送られたワンタイムパスワード打ち込み
class PwwsrP(forms.Form):
    otp=forms.CharField(label="メールに送られてきたワンタイムパスワード",max_length=5)