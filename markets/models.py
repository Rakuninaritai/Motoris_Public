from django.db import models
from django.conf import settings
# カスタムモデル仕様のためUserimport仕方変更
# settingsにカスタムユーザーモデルが指定してあるのでそれを参照するようにさせる(拡張ユーザーモデルなのでカスタム指定で元のも引っ張れる。)
from django.conf import settings

class Product(models.Model):
    staus_choices=[
        (1,'出品中'),
        (2,'購入完了'),
        (31,'購入後1'),
        (32,'購入後2'),
        (33,'購入後3'),
        (34,'購入後4'),
        (35,'購入後5'),
        (36,'購入後6'),
        (37,'購入後7'),
        (38,'購入後8'),
        (39,'購入後9'),
        (4,'終了'),
    ]
    title = models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    freetext = models.TextField(default="freetext")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', )
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)

    def __str__(self):
        return self.title
    @property
    def class_name(self):
        return self.__class__.__name__
    
class Product_car(models.Model):
    staus_choices=[
        (1,'出品中'),
        (2,'購入完了'),
        (31,'購入後1'),
        (32,'購入後2'),
        (33,'購入後3'),
        (34,'購入後4'),
        (35,'購入後5'),
        (36,'購入後6'),
        (37,'購入後7'),
        (38,'購入後8'),
        (39,'購入後9'),
        (4,'終了'),
    ]
    title = models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    freetext = models.TextField(default="freetext")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_car')
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)

    def __str__(self):
        return self.title
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__

class Product_by(models.Model):
    staus_choices=[
        (1,'出品中'),
        (2,'購入完了'),
        (31,'購入後1'),
        (32,'購入後2'),
        (33,'購入後3'),
        (34,'購入後4'),
        (35,'購入後5'),
        (36,'購入後6'),
        (37,'購入後7'),
        (38,'購入後8'),
        (39,'購入後9'),
        (4,'終了'),
    ]
    title = models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    freetext = models.TextField(default="freetext")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_by')
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)

    def __str__(self):
        return self.title
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__


class Product_mc(models.Model):
    staus_choices=[
        (1,'出品中'),
        (2,'購入完了'),
        (31,'購入後1'),
        (32,'購入後2'),
        (33,'購入後3'),
        (34,'購入後4'),
        (35,'購入後5'),
        (36,'購入後6'),
        (37,'購入後7'),
        (38,'購入後8'),
        (39,'購入後9'),
        (4,'終了'),
    ]
    title = models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    freetext = models.TextField(default="freetext")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_mc', )
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)

    def __str__(self):
        return self.title
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # 同じユーザーが同じプロダクトに複数回いいねできないように

