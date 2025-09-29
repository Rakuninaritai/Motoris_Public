from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EventPost, Comment, UploadImageModel
from datetime import datetime, timedelta
from django.utils import timezone
from django.forms import ClearableFileInput
    
class EventPostForm(forms.ModelForm):
    
    # images = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    #     required=True,
    #     label="画像"
    # )
    class Meta:
        model = EventPost
        fields = ['title', 'free_text', 'prefecture_field', 'address', 'event_date', 'start_time', 'end_time', ]
    
        
    title = forms.CharField(label='タイトル',
                            widget=forms.TextInput(attrs={'placeholder': 'タイトルを入力してください...'}))
    
    address = forms.CharField(label='住所',
                            widget=forms.TextInput(attrs={'placeholder': '例:小樽市花園2丁目1-1...'}))
    
    free_text = forms.CharField(label='説明',
                            widget=forms.Textarea(attrs={'maxlength': '1000'}), required=True)
    
    event_date = forms.DateField(label='開催日程',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'onfocus': 'this.showPicker()'}))
            
    start_time = forms.TimeField(
        widget=forms.Select(
            choices=[
                ('', '開始時間を選択...'),
                ('09:00', '09:00'),
                ('10:00', '10:00'),
                ('11:00', '11:00'),
                ('12:00', '12:00'),
                ('13:00', '13:00'),
                ('14:00', '14:00'),
                ('15:00', '15:00'),
                ('16:00', '16:00'),
                ('17:00', '17:00'),
                ('18:00', '18:00'),
                ('19:00', '19:00'),
                ('20:00', '20:00'),
                ('21:00', '21:00'),
                ('22:00', '22:00'),
                ('23:00', '23:00'),
                ('24:00', '24:00'),
            ]
        ),
        required=True,
        initial='13:00'
        )

    end_time = forms.TimeField(
        widget=forms.Select(
            choices=[
                ('', '終了時間を選択...'),  # 初期状態の選択肢
                ('09:00', '09:00'),
                ('10:00', '10:00'),
                ('11:00', '11:00'),
                ('12:00', '12:00'),
                ('13:00', '13:00'),
                ('14:00', '14:00'),
                ('15:00', '15:00'),
                ('16:00', '16:00'),
                ('17:00', '17:00'),
                ('18:00', '18:00'),
                ('19:00', '19:00'),
                ('20:00', '20:00'),
                ('21:00', '21:00'),
                ('22:00', '22:00'),
                ('23:00', '23:00'),
                ('24:00', '24:00'),  # ここで24時を追加
            ]
        ),
        required=True,
        initial='18:00'
    )

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prefecture_field'].widget.attrs.update({
            'style': 'width: 100%; height: 40px; margin-bottom:10px',
            })
            
    prefecture_field = forms.ChoiceField(label='都道府県',
                                         choices=[
                                            ('','未選択...'),
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
                                            ('徳島県', ' 徳島県'),
                                            ('香川県', ' 香川県'),
                                            ('愛媛県', ' 愛媛県'),
                                            ('高知県', ' 高知県'),
                                            ('福岡県', '福岡県'),
                                            ('佐賀県', '佐賀県'),
                                            ('長崎県', '長崎県'),
                                            ('熊本県', '熊本県'),
                                            ('大分県', '大分県'),
                                            ('宮崎県', '宮崎県'),
                                            ('鹿児島県', '鹿児島県'),
                                            ('沖縄県', '沖縄県'),])
    
    widgets = {
        'event_date': forms.DateTimeInput(attrs={
            'type': 'datetime-local'
            }),
    }
    
class EventImageForm(forms.ModelForm):
    class Meta:
        model = UploadImageModel
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

#検索
class EventSearchForm(forms.Form):
        
    REGION_CHOICES = [
        ('','指定なし'),
        ('北海道地方', '北海道地方'),
        ('北海道', '　北海道'),
        ('東北地方', '東北地方'),
        ('青森県', '　青森県'),
        ('岩手県', '　岩手県'),
        ('宮城県', '　宮城県'),
        ('秋田県', '　秋田県'),
        ('山形県', '　山形県'),
        ('福島県', '　福島県'),
        ('関東地方', '関東地方'),
        ('茨城県', '　茨城県'),
        ('栃木県', '　栃木県'),
        ('群馬県', '　群馬県'),
        ('埼玉県', '　埼玉県'),
        ('千葉県', '　千葉県'),
        ('東京都', '　東京都'),
        ('神奈川県', '　神奈川県'),
        ('北陸地方', '北陸地方'),
        ('新潟県', '　新潟県'),
        ('富山県', '　富山県'),
        ('石川県', '　石川県'),
        ('福井県', '　福井県'),
        ('中部地方', '中部地方'),
        ('山梨県', '　山梨県'),
        ('長野県', '　長野県'),
        ('岐阜県', '　岐阜県'),
        ('静岡県', '　静岡県'),
        ('愛知県', '　愛知県'),
        ('近畿地方', '近畿地方'),
        ('三重県', '　三重県'),
        ('滋賀県', '　滋賀県'),
        ('京都府', '　京都府'),
        ('大阪府', '　大阪府'),
        ('兵庫県', '　兵庫県'),
        ('奈良県', '　奈良県'),
        ('和歌山県', '　和歌山県'),
        ('中国地方', '中国地方'),
        ('鳥取県', '　鳥取県'),
        ('島根県', '　島根県'),
        ('岡山県', '　岡山県'),
        ('広島県', '　広島県'),
        ('山口県', '　山口県'),
        ('四国地方', '四国地方'),
        ('徳島県', ' 　徳島県'),
        ('香川県', ' 　香川県'),
        ('愛媛県', ' 　愛媛県'),
        ('高知県', ' 　高知県'),
        ('九州地方', '九州地方'),
        ('福岡県', '　福岡県'),
        ('佐賀県', '　佐賀県'),
        ('長崎県', '　長崎県'),
        ('熊本県', '　熊本県'),
        ('大分県', '　大分県'),
        ('宮崎県', '　宮崎県'),
        ('鹿児島県', '　鹿児島県'),
        ('沖縄県', '沖縄県'),
    ]

    region = forms.ChoiceField(choices=REGION_CHOICES, required=False, label='地域')
    
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['year_month'].choices = self.get_year_month_choices()

    def get_year_month_choices(self):
        choices = []
        current_date = timezone.now().date()
        for i in range(12):
            date = current_date + timedelta(days=30*i)
            value = date.strftime('%Y-%m')
            label = date.strftime('%Y年%m月')
            choices.append((value, label))
        return choices
    
    year_month = forms.ChoiceField(required=False, label='年月')
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','comment_image']
        
    content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'コメントを入力...'}))
    comment_image = forms.ImageField(required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'style': 'display:none;'}))