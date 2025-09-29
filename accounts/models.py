from django.db import models
from django.templatetags.static import static
# ユーザーモデルを拡張できるやつをインポート
from django.contrib.auth.models import AbstractUser
# カスタムモデル仕様のためUserimport仕方変更
# settingsにカスタムユーザーモデルが指定してあるのでそれを参照するようにさせる(拡張ユーザーモデルなのでカスタム指定で元のも引っ張れる。)
from django.conf import settings


# Create your models here.

# emailの重複排除のための拡張(absteruserは拡張)
class CustomUser(AbstractUser):
     # emailのユニークをトゥルーに
     email = models.EmailField(unique=True)



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='.',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)

    def get_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return static('images/default_account.png')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    

# ほかモデルでUserを呼び出すときはめんどいけど↓でお願いします
# # カスタムモデル仕様のためUserimport仕方変更
#from django.contrib.auth import get_user_model
#User = get_user_model()