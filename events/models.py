from django.db import models
from django import forms
from django.utils import timezone
# settingsにカスタムユーザーモデルが指定してあるのでそれを参照するようにさせる(拡張ユーザーモデルなのでカスタム指定で元のも引っ張れる。)
from django.conf import settings
    
class EventPost(models.Model):
    title = models.CharField(max_length=100)
    event_date = models.DateField('event date')
    start_time = models.TimeField(default="13:00")
    end_time = models.TimeField(default="18:00")
    address = models.CharField(max_length=255,blank=True)
    free_text = models.TextField()
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
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
    
    prefecture_field = models.CharField(max_length=10, choices=PREFECTURES,default='北海道')
    
    #都道府県の入力から地方も特定する
    def get_region(self):
        prefecture = self.prefecture_field
        if prefecture in ['北海道']:
            return '北海道地方'
        elif prefecture in ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県']:
            return '東北地方'
        elif prefecture in ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県']:
            return '関東地方'
        elif prefecture in ['新潟県', '富山県', '石川県', '福井県']:
            return '北陸地方'
        elif prefecture in ['山梨県', '長野県']:
            return '中部地方'
        elif prefecture in ['岐阜県', '静岡県', '愛知県']:
            return '中部地方'
        elif prefecture in ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県']:
            return '近畿地方'
        elif prefecture in ['鳥取県', '島根県', '岡山県', '広島県', '山口県']:
            return '中国地方'
        elif prefecture in ['徳島県', '香川県', '愛媛県', '高知県']:
            return '四国地方'
        elif prefecture in ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県']:
            return '九州地方'
        elif prefecture in ['沖縄県']:
            return '沖縄地方'
        else:
            return '不明'

class UploadImageModel(models.Model):
    event_post = models.ForeignKey(EventPost, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True,blank=True,default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Image for {self.event_post.title}"
    
    
#参加予定
class EventEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(EventPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')   #同じユーザーが同じイベントに参加できないようにする
        
        
        
class Comment(models.Model):
    post = models.ForeignKey(EventPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_image = models.ImageField(upload_to='event_comment_images/', null=True)

    def __str__(self):
        return self.text[:20]