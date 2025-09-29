#テンプレで扱えないものをこっちで扱う
# このフォルダ名じゃなきゃダメでアプリにないとダメ(テンプは離れててもloadファイル名で探しに来る)

# テンプレートライブラリーを呼ぶのにimport
from django import template

# 今回の処理を登録するテンプレートライブラリーを呼び出しregisterにin
register = template.Library()

# ↓でテンプレでも使える関数になる
@register.filter
# loginのエラーメッセージデフォルトでユーザー名をユーザー名またはメールアドレスにするのとまとめてエラーよこすので。で改行させる関数
def yuzameru_kaigyo(value):
  if "ユーザー名" in value:
        # 置き換えてくださいねユーザー名をユーザー名またはメールアドレスに
        value = value.replace("ユーザー名", "ユーザー名またはメールアドレス")
  #置き換えてくださいね。を。<br>に
  # value = value.replace("。", "。<br>")
  return value

# ↓でテンプレでも使える関数になる
@register.filter
def kaigyo(value):
  #置き換えてくださいね。を。<br>に
  # value = value.replace("。", "。<br>")
  return value

