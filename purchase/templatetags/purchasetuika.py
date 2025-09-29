#テンプレで扱えないものをこっちで扱う
# このフォルダ名じゃなきゃダメでアプリにないとダメ(テンプは離れててもloadファイル名で探しに来る)

# テンプレートライブラリーを呼ぶのにimport
from django import template


# 今回の処理を登録するテンプレートライブラリーを呼び出しregisterにin
register = template.Library()

# 文字数によって…を表示する関数
def mzsu(name,mx):
    value=name
    if(len(value)>mx):
        value=value[:mx]+"…"
    return value

# ↓でテンプレでも使える関数になる
@register.simple_tag
# 決済ページのモデルネームが文字数を超えたときに…を表示する
def KMN_mzsu(name):
    return mzsu(name,20)

# 決済完了ページの商品名が文字数超えたら
@register.simple_tag
def KKMN_mzsu(name):
    return mzsu(name,6)

# 購入後の商品名が文字数超えたら
@register.simple_tag
def KNMN_mzsu(name):
    return mzsu(name,13)

# 購入後のユーザーが文字数超えたら
@register.simple_tag
def KNU_mzsu(name):
    return mzsu(name,15)