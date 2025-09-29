from django.db import models
# カスタムモデル仕様のためUserimport仕方変更
# settingsにカスタムユーザーモデルが指定してあるのでそれを参照するようにさせる(拡張ユーザーモデルなのでカスタム指定で元のも引っ張れる。)
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# 各infomodelの@propaty残すのと、bikeにも付けてほしいshuto

# 統一項目外だし(スクロールが大変だったのでshuto)
CONDITION = [
        ('非常に良い','非常に良い'),
        ('良い','良い'),
        ('悪い','悪い'),
        ('非常に悪い','非常に悪い'),
    ]
PREFECTURES = [
        ('北海道', '北海道'),
        ('青森県', '青森県'),
        ('岩手県', '岩手県'),
        ('宮城県', '宮城県'),
        ('秋田県', '秋田県'),
        ('山形県', '山形県'),
        ('福島県', '福島県'),
        ('茨城県', '茨城県'),
        ('栃木県', '栃木県'),
        ('群馬県', '群馬県'),
        ('埼玉県', '埼玉県'),
        ('千葉県', '千葉県'),
        ('東京都', '東京都'),
        ('神奈川県', '神奈川県'),
        ('新潟県', '新潟県'),
        ('富山県', '富山県'),
        ('石川県', '石川県'),
        ('福井県', '福井県'),
        ('山梨県', '山梨県'),
        ('長野県', '長野県'),
        ('岐阜県', '岐阜県'),
        ('静岡県', '静岡県'),
        ('愛知県', '愛知県'),
        ('三重県', '三重県'),
        ('滋賀県', '滋賀県'),
        ('京都府', '京都府'),
        ('大阪府', '大阪府'),
        ('兵庫県', '兵庫県'),
        ('奈良県', '奈良県'),
        ('和歌山県', '和歌山県'),
        ('鳥取県', '鳥取県'),
        ('島根県', '島根県'),
        ('岡山県', '岡山県'),
        ('広島県', '広島県'),
        ('山口県', '山口県'),
        ('徳島県', '徳島県'),
        ('香川県', '香川県'),
        ('愛媛県', '愛媛県'),
        ('高知県', '高知県'),
        ('福岡県', '福岡県'),
        ('佐賀県', '佐賀県'),
        ('長崎県', '長崎県'),
        ('熊本県', '熊本県'),
        ('大分県', '大分県'),
        ('宮崎県', '宮崎県'),
        ('鹿児島県', '鹿児島県'),
        ('沖縄県', '沖縄県'),
    ]

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




class MotorcycleModel(models.Model):
    MAKER = [
        ('HONDA','HONDA'),
        ('Kawasaki','Kawasaki'),
        ('YAMAHA','YAMAHA'),
        ('SUZUKI','SUZUKI'),
        ('Harley-Davidson','Harley-Davidson'),
        ('BMW','BMW'),
        ('Triumph','Triumph'),
        ('Ducati','Ducati'),
        ('KTM','KTM'),
        ('Royal Enfield','Royal Enfield'),
        ('Indian','Indian'),
        ('その他','その他'),
    ]
    DISPLACEMENT = [
        ('50cc以下','50cc以下'),
        ('51~125cc','51~125cc'),
        ('126~250cc','126~250cc'),
        ('251~400cc','251~400cc'),
        ('401~750cc','401~750cc'),
        ('751cc以上','751cc以上'),
    ]
    maker = models.CharField(max_length=30, choices=MAKER)
    displacement = models.CharField(max_length=10, choices=DISPLACEMENT)
    name = models.CharField(max_length=50)
    type = models.IntegerField()
    number = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.name} ({self.maker}, {self.displacement})"

class MCInfoModel(models.Model):
    MAKER = [
        ('HONDA','HONDA'),
        ('Kawasaki','Kawasaki'),
        ('YAMAHA','YAMAHA'),
        ('SUZUKI','SUZUKI'),
    ]
    DISPLACEMENT = [
        ('50cc以下','50cc以下'),
        ('51~125cc','51~125cc'),
        ('126~250cc','126~250cc'),
        ('251~400cc','251~400cc'),
        ('401~750cc','401~750cc'),
        ('751cc以上','751cc以上'),
    ]
   
    
    DOCUMENTS = [
        ('あり','あり'),
        ('なし','なし'),
    ]
    
    maker=models.CharField(max_length=30,choices=MAKER,default='HONDA')
    displacement=models.CharField(max_length=10,choices=DISPLACEMENT,default='50cc以下')
    modelname = models.ForeignKey(MotorcycleModel, on_delete=models.SET_NULL, null=True, blank=True)
    price=models.IntegerField(blank=False)
    explanation=models.TextField(max_length=1000,blank=False)
    mileage=models.IntegerField(blank=True,null=True)
    modelyear=models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)],blank=True,null=True)
    number=models.IntegerField(blank=True,null=True)
    documents=models.CharField(max_length=2,choices=DOCUMENTS,default='あり')
    vehicleinspection=models.CharField(max_length=2,choices=DOCUMENTS,default='なし')
    vehicleinspectiondate=models.CharField(max_length=10,blank=True,null=True)
    condition=models.CharField(max_length=10,choices=CONDITION,default='非常に良い')
    prefectures=models.CharField(max_length=10,choices=PREFECTURES,default='北海道')
    type=models.IntegerField(null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    soldflag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)
    
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__
    


#TestModel
class MCImageModel(models.Model):
    testmotorcycle = models.ForeignKey(MCInfoModel,related_name='images',on_delete=models.CASCADE,null=True)
    files =models.ImageField('画像ファイル',null=True,blank=True,default='')

class CarModel(models.Model):
    MAKER = [
        ('TOYOTA','TOYOTA'),
        ('HONDA','HONDA'),
        ('NISSAN','NISSAN'),
        ('MATUDA','MATUDA'),
        ('MITUBISI','MITUBISI'),
        ('SUBARU','SUBARU'),
        ('DAIHATU','DAIHATU'),
        ('SUZUKI','SUZUKI'),
    ]
    maker = models.CharField(max_length=30, choices=MAKER)
    name = models.CharField(max_length=50)
    type = models.IntegerField()
    number = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.name} ({self.maker})"

class CInfoModel(models.Model):
    MAKER = [
        ('TOYOTA','TOYOTA'),
        ('HONDA','HONDA'),
        ('NISSAN','NISSAN'),
        ('MATUDA','MATUDA'),
        ('MITUBISI','MITUBISI'),
        ('SUBARU','SUBARU'),
        ('DAIHATU','DAIHATU'),
        ('SUZUKI','SUZUKI'),
    ]
   
    DOCUMENTS = [
        ('あり','あり'),
        ('なし','なし'),
    ]
    MISSION = [
        ('MT','MT'),
        ('AT','AT'),
        ('CVT','CVT'),
        ('DCT','DCT'),
        ('AMT','AMT'),
    ]
    COLOR = [
        ('ホワイト系','ホワイト系'),
        ('ゴールド・シルバー系','ゴールド・シルバー系'),
        ('ブラック系','ブラック系'),
        ('ガンメタ系','ガンメタ系'),
        ('グレー系','グレー系'),
        ('レッド系','レッド系'),
        ('グリーン系','グリーン系'),
        ('ワイン系','ワイン系'),
        ('ブルー系','ブルー系'),
        ('イエロー系','イエロー系'),
        ('オレンジ系','オレンジ系'),
        ('パープル系','パープル系'),
        ('ピンク系','ピンク系'),
        ('ブラウン系','ブラウン系'),
        ('その他','その他'),
    ]

    maker=models.CharField(max_length=30,choices=MAKER,default='TOYOTA')
    modelname=models.ForeignKey('CarModel',on_delete=models.SET_NULL,null=True)
    price=models.IntegerField()
    explanation=models.TextField(max_length=1000)
    mileage=models.IntegerField(blank=True,null=True)
    modelyear=models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)],blank=True,null=True)
    number=models.IntegerField(blank=True,null=True)
    vehicleinspection=models.CharField(max_length=10)
    condition=models.CharField(max_length=10,choices=CONDITION,default='非常に良い')
    prefectures=models.CharField(max_length=10,choices=PREFECTURES,default='北海道')
    type=models.IntegerField(blank=True,null=True)
    mission=models.CharField(max_length=3,choices=MISSION,default='AT')
    color=models.CharField(max_length=10,choices=COLOR,default='ホワイト系')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    soldflag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)
    
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__
    

class CImageModel(models.Model):
    testcar = models.ForeignKey(CInfoModel,related_name='images',on_delete=models.CASCADE,null=True)
    files = models.ImageField('画像ファイル',null=True,blank=True,default='')


class BInfoModel(models.Model):
    MAKER = [
        ('BRIDGESTONE','BRIDGESTONE'),
        ('Panasonic','Panasonic'),
        ('MIYATA','MIYATA'),
    ]
    
    
    maker=models.CharField(max_length=30,choices=MAKER,default='BRIDGESTONE')
    modelname=models.CharField(max_length=50)
    price=models.IntegerField()
    explanation=models.TextField(max_length=1000)
    condition=models.CharField(max_length=10,choices=CONDITION,default='非常に良い')
    prefectures=models.CharField(max_length=10,choices=PREFECTURES,default='北海道')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    soldflag=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # 状態
    status=models.IntegerField(choices=staus_choices,default=1)
    
    # models名を呼び出せるようにするために以下記述(xx(viewsからテンプに渡す変数名).class_nameで取得可能)
    @property
    def class_name(self):
        return self.__class__.__name__

class BImageModel(models.Model):
    testbike = models.ForeignKey(BInfoModel,related_name='images',on_delete=models.CASCADE,null=True)
    files = models.ImageField('画像ファイル',null=True,blank=True,default='')

    

# class bikeshuppin(models.Model):
#     MAKER = [
#         ('BRIDGESTONE','BRIDGESTONE'),
#         ('Panasonic','Panasonic'),
#         ('MIYATA','MIYATA'),
#     ]
#     CONDITION = [
#         ('非常に良い','非常に良い'),
#         ('良い','良い'),
#         ('悪い','悪い'),
#         ('非常に悪い','非常に悪い'),
#     ]
#     PREFECTURES = [
#         ('北海道', '北海道'),
#         ('青森県', '青森県'),
#         ('岩手県', '岩手県'),
#         ('宮城県', '宮城県'),
#         ('秋田県', '秋田県'),
#         ('山形県', '山形県'),
#         ('福島県', '福島県'),
#         ('茨城県', '茨城県'),
#         ('栃木県', '栃木県'),
#         ('群馬県', '群馬県'),
#         ('埼玉県', '埼玉県'),
#         ('千葉県', '千葉県'),
#         ('東京都', '東京都'),
#         ('神奈川県', '神奈川県'),
#         ('新潟県', '新潟県'),
#         ('富山県', '富山県'),
#         ('石川県', '石川県'),
#         ('福井県', '福井県'),
#         ('山梨県', '山梨県'),
#         ('長野県', '長野県'),
#         ('岐阜県', '岐阜県'),
#         ('静岡県', '静岡県'),
#         ('愛知県', '愛知県'),
#         ('三重県', '三重県'),
#         ('滋賀県', '滋賀県'),
#         ('京都府', '京都府'),
#         ('大阪府', '大阪府'),
#         ('兵庫県', '兵庫県'),
#         ('奈良県', '奈良県'),
#         ('和歌山県', '和歌山県'),
#         ('鳥取県', '鳥取県'),
#         ('島根県', '島根県'),
#         ('岡山県', '岡山県'),
#         ('広島県', '広島県'),
#         ('山口県', '山口県'),
#         ('徳島県', '徳島県'),
#         ('香川県', '香川県'),
#         ('愛媛県', '愛媛県'),
#         ('高知県', '高知県'),
#         ('福岡県', '福岡県'),
#         ('佐賀県', '佐賀県'),
#         ('長崎県', '長崎県'),
#         ('熊本県', '熊本県'),
#         ('大分県', '大分県'),
#         ('宮崎県', '宮崎県'),
#         ('鹿児島県', '鹿児島県'),
#         ('沖縄県', '沖縄県'),
#     ]
    
#     maker=models.CharField(max_length=30,choices=MAKER,default='BRIDGESTONE')
#     modelname=models.CharField(max_length=50)
#     price=models.IntegerField()
#     explanation=models.TextField(max_length=1000)
#     condition=models.CharField(max_length=10,choices=CONDITION,default='非常に良い')
#     prefectures=models.CharField(max_length=10,choices=PREFECTURES,default='北海道')
    
# class bikeImage(models.Model):
#     bike = models.ForeignKey(bikeshuppin, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='medea/images/')

#     def __str__(self):
#         return f"Image for {self.bike.modelname}"
