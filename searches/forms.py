from django import forms
from shuppin.models import MCInfoModel,MCImageModel,CInfoModel,CImageModel,MotorcycleModel,CarModel,BInfoModel,BImageModel#,Bikemodel
from datetime import datetime

# 年代用関数
def choiy(gen):
  return [("",f"{gen}なし")]+[(str(year),str(year))for year in range(1950,datetime.now().year+1)]


# 全部で必要な項目をまとめてるbaseform
class BaseForm(forms.Form):
  # 年代(上下)、価格(上下)は統一なのでこのベースを継承させる
  
  modelyear_min=forms.ChoiceField(
      # 上の年代用関数を使っている
      choices=choiy("下限"),
      # 必須ではない,何もないとNoneを返す
      required=False,
      label="年代(下限)"
    )
    
  modelyear_max = forms.ChoiceField(
          choices=choiy("上限"),
          required=False,
          label="年代(上限)"
      )
    
  price_min = forms.ChoiceField(
    # formのchoiceはvalue,label
          choices=[
              ('', '下限なし'),
              ('0', '0円'),
              ('50000', '50,000円'),
              ('100000', '100,000円'),
              ('300000', '300,000円'),
              ('500000', '500,000円'),
              ('1000000', '1,000,000円'),
          ],
          required=False,
          label="価格(下限)"
      )
    
  price_max = forms.ChoiceField(
          choices=[
              ('', '上限なし'),
              ('50000', '50,000円'),
              ('100000', '100,000円'),
              ('300000', '300,000円'),
              ('500000', '500,000円'),
              ('1000000', '1,000,000円'),
              ('5000000', '5,000,000円'),
          ],
          required=False,
          label="価格(上限)"
      )
  # formバリデーションを追加したいときはclean
  def clean(self):
    # 全ての項目に基本的なバリデーションを実行しcleanedに格納
    cleaned_data=super().clean()
    # 各データを取得(データがない場合はnone(required=falseだから))
    modelyear_min = cleaned_data.get('modelyear_min')
    modelyear_max = cleaned_data.get('modelyear_max')
    price_min = cleaned_data.get('price_min')
    price_max = cleaned_data.get('price_max')
    
    # # minもmaxもtrue(値がある)でmaxのがminより小さければ
    # if modelyear_min and modelyear_max and int(modelyear_min) > int(modelyear_max):
    #   # バリデーションエラーとしてください。(raiseは例外処理を書きたいときにつかう)
    #   raise forms.ValidationError("年代の下限が上限を超えています。")
    
    # if price_min and price_max and int(price_min)>int(price_max):
    #   raise forms.ValidationError("価格の下限が上限を超えています。")
    
    
    
     # 年代の下限が上限を超えていないか
    #  モデルイヤーの両方に値があれば
    if modelyear_min and modelyear_max  :
        # どちらも空文字でない場合に整数変換
      modelyear_min = int(modelyear_min)
      modelyear_max = int(modelyear_max)
      # min,max逆なら
      if modelyear_min > modelyear_max:
        # エラーを追加してcleand.dateに
          self.add_error('modelyear_min', "年代の下限が上限を超えています。")

    # 価格の下限が上限を超えていないか
    if price_min and price_max  :
      # どちらも空文字でない場合に整数変換
      price_min = int(price_min)
      price_max = int(price_max)
      if price_min > price_max:
          self.add_error('price_min', "価格の下限が上限を超えています。")

    return cleaned_data
    
    # formがエラーになるとそのフォームのエラーずに格納される
    # {% if form.errors %}
    #     <ul style="color: red;">
    #         {% for error in form.errors %}
    #             <li>{{ error }}</li>
    #         {% endfor %}
    #     </ul>
    # {% endif %}



class MCsf(BaseForm):
  maker=forms.ChoiceField(
    # 選択肢は出品のモデルから流用
    # 選択なしも追加
    choices=[('', '選択なし')] + list(MotorcycleModel.MAKER),
    # 必須ではない,何もないとNoneを返す
    required=False,
    label="メーカー"
  )
  displacement = forms.ChoiceField(
        choices=[('', '選択なし')] + list(MotorcycleModel.DISPLACEMENT),
        required=False,
        label="排気量"
    )
  modelname = forms.ModelChoiceField(
    # デフォルトはnoneでメーカー排気量で動的に
        queryset=MotorcycleModel.objects.none(),
        required=False,
        label="商品名"
    )
  
  # post時に商品のフィールドに入力データを保持させる処理
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelname'].queryset = MotorcycleModel.objects.none()
        if 'maker' in self.data and 'displacement' in self.data:
            maker = self.data.get('maker')
            displacement = self.data.get('displacement')
            self.fields['modelname'].queryset = MotorcycleModel.objects.filter(
                maker=maker, displacement=displacement
            )

class Carsf(BaseForm):
    maker=forms.ChoiceField(
    # 選択肢は出品のモデルから流用
    # 選択なしも追加
    choices=[('', '選択なし')] + list(CarModel.MAKER),
    # 必須ではない,何もないとNoneを返す
    required=False,
    label="メーカー"
      )
    modelname = forms.ModelChoiceField(
      # デフォルトはnoneでメーカー排気量で動的に
          queryset=CarModel.objects.none(),
          required=False,
          label="商品名"
      )
    
    color=forms.ChoiceField(
    # 選択肢は出品のモデルから流用
    # 選択なしも追加
    choices=[('', '選択なし')] + list(CInfoModel.COLOR),
    # 必須ではない,何もないとNoneを返す
    required=False,
    label="カラー"
      )
  
    # post時に商品のフィールドに入力データを保持させる処理
    def __init__(self,*args,**kwargs):
          super().__init__(*args,**kwargs)
          self.fields['modelname'].queryset = CarModel.objects.none()
          current_year = datetime.now().year
          years = [(year,str(year)) for year in range(1950,current_year+1)]
          # self.fields['modelyear'] = forms.ChoiceField(choices=years)
          
          if 'maker' in self.data:
              maker = self.data.get('maker')
              self.fields['modelname'].queryset = CarModel.objects.filter(maker=maker)
              

class Bysf(BaseForm):
  maker=forms.ChoiceField(
    choices=[('', '選択なし')] + list(BInfoModel.MAKER),
    # 必須ではない,何もないとNoneを返す
    required=False,
    label="メーカー"
      )
  modelname = forms.CharField(
    # デフォルトはnoneでメーカー排気量で動的に
        required=False,
        label="商品名"
    )