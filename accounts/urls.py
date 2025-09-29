from django.urls import path
# topviewで定義している404ページをレンダリングする処理をimport
from top.views import custom_404_view

# 必要なURL以外を無効か(404)
urlpatterns = [
     # メニューとして表示されていたページの404確認済み
     path('signup/', custom_404_view,
         name='account_signup'),
     path('login/', custom_404_view,
         name='account_login'),
     path('logout/', custom_404_view,
         name='account_logout'),
     path('password/change/', custom_404_view,
         name='account_change_password'),
     path('password/set/', custom_404_view,
         name='account_set_password'),
     path('password/reset/', custom_404_view,
         name='account_reset_password'),
     path('password/reset/done/',custom_404_view,
         name='account_reset_password_done'),
     path('password/reset/key/done/',custom_404_view,
         name='account_reset_password_from_key_done'),
     path('inactive/',custom_404_view,
         name='account_inactive'),
]

"""
  templates_allauth
|
└── socialaccount/
    └── authentication_error.html  # ソーシャルログインエラー用
    └── signup.html          # サインアップページ用テンプレート
"""