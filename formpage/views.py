from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import ContactInfo
# メール送信用
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse


class FormView(TemplateView):
    # 初期変数定義
    def __init__(self):
        self.params = {"Message": "情報を入力してください。",
                       "form": forms.Contact_Form(),
                       }

    # GET時の処理
    def get(self, request):
        return render(request, "formpage/formpage.html", context=self.params)

    # POST時の処理
    def post(self, request):
        if request.method == "POST":
            self.params["form"] = forms.Contact_Form(request.POST)

            # フォーム入力が有効な場合
            if self.params["form"].is_valid():
                self.params["Message"] = "入力情報が送信されました。"

                # ユーザーIDを取得（ログインしていない場合はNoneを設定）
                user_id = request.user if request.user.is_authenticated else None

                # フォームの情報をモデルに保存
                ContactInfo.objects.create(
                    Name=self.params["form"].cleaned_data['Name'],
                    Tell=self.params["form"].cleaned_data['Tell'],
                    Mail=self.params["form"].cleaned_data['Mail'],
                    Text=self.params["form"].cleaned_data['Text'],
                    user_id=user_id  # ログインしていればユーザーIDを保存、していなければNone
                )

                # 成功後、topページへリダイレクト
                return redirect('top')  # top.htmlに対応するURL名にリダイレクト

        return render(request, "formpage/formpage.html", context=self.params)
    
# 管理ページ
class FormAdminView(UserPassesTestMixin,TemplateView):
    template_name = 'formpage/formadmin.html'
    
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        # ContactInfoのデータを全て取得
        context = super().get_context_data(**kwargs)
        context['contact_info_list'] = ContactInfo.objects.all()
        return context
    

# 回答メールのフォームを表示するビュー
def send_mail_form(request, contact_id):
    # ContactInfoの情報を取得
    contact = get_object_or_404(ContactInfo, id=contact_id)

    # フォームに送るためのコンテキストを作成
    return render(request, 'formpage/sendmail.html', {'contact': contact})

# メール送信処理を行うビュー
def send_reply(request, contact_id):
    # ContactInfoの情報を取得
    contact = get_object_or_404(ContactInfo, id=contact_id)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = [contact.Mail]

        # 送信元のメールアドレスを指定
        from_email = 'NH24.IAIH.J@gmail.com'

        # メール送信
        send_mail(
            subject,
            message,
            from_email,  
            recipient_list,  # 受信者リスト
            fail_silently=False,
        )

        # メール送信後、管理ページにリダイレクト
        return redirect(reverse('formadmin'))  # 管理ページへのリダイレクト

    # POST以外のリクエストには対応しない
    return HttpResponse("不正なリクエストです。", status=400)
