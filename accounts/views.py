from django.shortcuts import render, redirect
from django.contrib import messages
# ログインの関数
from django.contrib.auth import login
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.conf import settings

from .forms import UserRegisterForm,PwwsrM,PwwsrP
from .models import Profile
from profiles.forms import ProfileForm
from django.views import View
# viewはユーザーモデルを取得してして使用することが出来る(modelはdjangoが立ち上がる上がる前から読み込まないといけないから取得できない)
from django.contrib.auth import get_user_model
# ランダムな文字列を返す(otp用)
from django.utils.crypto import get_random_string
# メール送信用
from django.core.mail import send_mail

# Create your views here.

# modelで指定しているuserのsettingsは文字列を返すのに対しこちらは実際のモデルを返すので適している
CustomUser = get_user_model()

#ユーザー登録

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            #作成時にProfileが存在しない場合のみ作成　エラー回避のため
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# LoginとLogoutviewはメッセージを出すためだけに書いてます
class LoginView(LoginView):
    # formが正しければ(ログイン出来たら)
    def form_valid(self, form):
        username = form.get_user().username
        messages.success(self.request, f"Hello {username}, you're now logged in!")
        # 指定の場所へ飛ぶnextならnext,topならtop
        return super().form_valid(form)
class LogoutView(LogoutView):
    # Logoutが呼び出されたらディスパッチ実行される
    def dispatch(self, request, *args, **kwargs):
        username=request.user.username
        # ログアウトする直前にメッセージをセット
        messages.success(request, f"See you next time, {username}! You've signed out successfully.")
        # dispatchの処理実行↓
        return super().dispatch(request, *args, **kwargs)
# パスワード忘れ用
class Pwwsr(View):
    
    def get(self,request):
        # メルアドフォーム
        form=PwwsrM()
        # エラー
        errors=""
        # 状態(メルアド入力がo,otp入力が1)
        zti=0
        return render(request,"accounts/pwwsr.html",{"form":form,"errors":errors,"zti":zti})
    # フォームが送られたら
    def post(self,request):
        # メルアドが送られたら
        if "email" in request.POST:
            # フォーム取得
            form=PwwsrM(request.POST)
            # フォームばりで
            if form.is_valid():
                # メルアド取得
                email = form.cleaned_data['email']
                try:
                    # そのユーザーを取得(メルアドから)
                    pwuser=CustomUser.objects.get(email=email)
                    # ランダムな文字列を返す(5文字以内)
                    otp=get_random_string(5)
                    # セッションでメルアド保存
                    request.session["email"]=email
                    # セッションでワンタイムパスワード保存
                    request.session["otp"]=otp
                    # セッションのメリットはdbに保存するまでもないデータの保存に適している(ブラウザ消すと消える、ユーザーログインもセッションの仕組み)
                    # 一日最大500通のメールが送れます
                    send_mail(
                        'Motorisワンタイムパスワード発行',  # 件名
                        f'ご利用いただきありがとうございます。\n切り替わったページで以下のワンタイムパスワードを入力してください。\n{otp}\n',  # メッセージ
                        'NH24.IAIH.J@gmail.com',  # 送信元のメールアドレス
                        [email],  # 送信先のメールアドレスのリスト
                        fail_silently=False, #falseでメールが送信できないと例外とする
                    )
                    return render(request,"accounts/pwwsr.html",{"form":PwwsrP(),"errors":"","zti":1})
                except:
                    # なければエラー
                    return render(request,"accounts/pwwsr.html",{"form":form,"errors":"そのメールアドレスのユーザーは存在しません","zti":0})
            else:
                return render(request,"accounts/pwwsr.html",{"form":form,"errors":"メールアドレスは正しく入力してください。","zti":0})
        if "otp" in request.POST:
            # フォーム取得
            form=PwwsrP(request.POST)
            # フォームばりで
            if form.is_valid():
                # 入力されたワンタイムパスワード取得
                otp = form.cleaned_data['otp']
                # メールに送信したワンタイムパスワード
                sotp=request.session.get("otp")
                # メルアド
                email=request.session.get("email")
                # ワンタイムパスワードがあっているか
                if str(sotp)==otp:
                    pwuser = CustomUser.objects.get(email=email)
                    
                    # ログイン処理(ログインバックエンドを指定)
                    login(request, pwuser, backend='django.contrib.auth.backends.ModelBackend')
                    # topに変わる
                    return redirect("top")
                else:
                    return render(request,"accounts/pwwsr.html",{"form":form,"errors":"ワンタイムパスワードが間違っています。","zti":1})
            else:
                return render(request,"accounts/pwwsr.html",{"form":form,"errors":"ワンタイムパスワードは正しく入力してください。","zti":1})