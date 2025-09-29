from django.db import models
from shuppin.models import BInfoModel, BImageModel, CInfoModel, CImageModel, MCInfoModel, MCImageModel
from django.db import models
from django.conf import settings
from shuppin.models import BInfoModel, CInfoModel, MCInfoModel

class Comment(models.Model):
    product_type = models.CharField(max_length=20)  # 'bike', 'car', 'motorBike' など
    product_id = models.IntegerField()  # 商品のID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='shohin_comments')  # 出品者またはログインユーザー
    guest_name = models.CharField(max_length=100, blank=True, null=True)  # ゲストユーザーの名前
    text = models.TextField()  # コメント内容
    created_at = models.DateTimeField(auto_now_add=True)  # コメント投稿日時

    def __str__(self):
        return f"Comment by {self.user or self.guest_name} on {self.product_type} {self.product_id}"
# shohin アプリケーション固有のモデルがなければ、このファイルは空でも構いません。
# shuppin のモデルを直接参照して使用します。

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # いいねしたユーザー
    product_type = models.CharField(max_length=20)  # 'bike', 'car', 'motorBike' など
    product_id = models.IntegerField()  # 商品のID
    created_at = models.DateTimeField(auto_now_add=True)  # いいねした日時

    class Meta:
        unique_together = ('user', 'product_type', 'product_id')  # ユーザーごとに1回しかいいねできないようにする

    def __str__(self):
        return f"Like by {self.user} on {self.product_type} {self.product_id}"