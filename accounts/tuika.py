#ここではメルアドでもユーザーでもログインできるのを書いていきます。
# あわよくばソーシャルログインも
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# 現在のUserモデルを取得
User = get_user_model()

# emailかusernameでログインできる用のクラス(settings.pyに追加してね)
class EmailOrUsernameBackend(ModelBackend):
  def authenticate(self, request, username=None, password=None, **kwargs):
    try:
            # ユーザー名またはメールアドレスで一致するユーザーを取得
            # ユーザーネームかemail(or条件)であったユーザーを取得
            user = User.objects.get(Q(username=username) | Q(email=username))
      # エラーが出たら(無ければ)
    except User.DoesNotExist:
            # 該当するユーザーがいない場合はNoneを返す
            return None
    # パスワードを検証し、有効ならユーザーを返す
    # パスワードをあっているか確認するのと(and)ユーザーが無効かされていないか確認
    if user.check_password(password) and self.user_can_authenticate(user):
            # okならユーザーを返す
            return user
    return None