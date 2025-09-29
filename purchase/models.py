from django.db import models
# カスタムモデル仕様のためUserimport仕方変更
# settingsにカスタムユーザーモデルが指定してあるのでそれを参照するようにさせる(拡張ユーザーモデルなのでカスタム指定で元のも引っ張れる。)
from django.conf import settings
from shuppin.models import MCInfoModel,MCImageModel,CInfoModel,CImageModel,BInfoModel,BImageModel
import datetime

# Create your models here.

# 統一項目外だし###
# 月選択肢
month_choises=[((i), f"{i:02}") for i in range(1, 13)]
# 年選択(今の年+10)
now_year=datetime.date.today().year
year_choises=[((i),f"{i}") for i in range(now_year,now_year+10)]

# 購入
# class Purchase(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # クレカゾーン#######
#     card_number=models.IntegerField()
#     # 有効期限
#     ketu_month=models.IntegerField(choices=month_choises)
#     # 年選択(今の年+10)
#     ketu_year=models.IntegerField(choices=year_choises)
#     # セキュリティコード
#     sec_code=models.IntegerField()
#     # カード名義人
#     card_meinin=models.CharField(max_length=100)
    
class Purchase_car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(CInfoModel, on_delete=models.CASCADE,related_name="car_product")
    created_at = models.DateTimeField(auto_now_add=True)
    # クレカゾーン#######
    card_number=models.IntegerField()
    # 有効期限
    ketu_month=models.IntegerField(choices=month_choises)
    # 年選択(今の年+10)
    ketu_year=models.IntegerField(choices=year_choises)
    # セキュリティコード
    sec_code=models.IntegerField()
    # カード名義人
    card_meinin=models.CharField(max_length=100)
    
    #写真
    im31 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im32 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im33 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im34 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im35 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im36 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im37 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    im38 = models.ImageField(upload_to="purchase_car/", null=True, blank=True)
    
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__
    
class Purchase_by(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(BInfoModel, on_delete=models.CASCADE,related_name="by_product")
    created_at = models.DateTimeField(auto_now_add=True)
    # クレカゾーン#######
    card_number=models.IntegerField()
    # 有効期限
    ketu_month=models.IntegerField(choices=month_choises)
    ketu_year=models.IntegerField(choices=year_choises)
    # セキュリティコード
    sec_code=models.IntegerField()
    # カード名義人
    card_meinin=models.CharField(max_length=100)
    
    # 写真
    im31 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    im32 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    im33 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    im34 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    im35 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    im36 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    im37 = models.ImageField(upload_to="purchase_by/", null=True, blank=True)
    
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__
    
class Purchase_mc(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(MCInfoModel, on_delete=models.CASCADE,related_name="mc_product")
    created_at = models.DateTimeField(auto_now_add=True)
    # クレカゾーン#######
    card_number=models.IntegerField()
    # 有効期限
    ketu_month=models.IntegerField(choices=month_choises)
    ketu_year=models.IntegerField(choices=year_choises)
    # セキュリティコード
    sec_code=models.IntegerField()
    # カード名義人
    card_meinin=models.CharField(max_length=100)
    
    # 写真
    im31 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    im32 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    im33 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    im34 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    im35 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    im36 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    im37 = models.ImageField(upload_to="purchase_mc/", null=True, blank=True)
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__