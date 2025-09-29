from django import forms
from django.forms import inlineformset_factory
# from .models import motorcycleshuppin,motorcycleImage,carshuppin,carImage,bikeshuppin,bikeImage
from .models import MCImageModel,MCInfoModel,MotorcycleModel,CImageModel,CInfoModel,CarModel,BImageModel,BInfoModel
from datetime import datetime

#TestModelForm
class MCImageForm(forms.ModelForm):
    class Meta:
        model = MCImageModel
        fields = ["files"]
        # 出品時なぜかformとして渡していない主キーとする外部キーの部分の必須エラーが出るので除外明示(modelを指定しているので通常は外部キーを必須にしなくてよい)
        exclude = ('testmotorcycle',)
        
#TestMotorcycleModelForm
class MCInfoForm(forms.ModelForm):
    class Meta:
        model = MCInfoModel
        fields = ["maker","displacement","modelname","price","explanation","modelyear","mileage","number","documents","vehicleinspection","vehicleinspectiondate","condition","prefectures"]  
        labels = {
            "maker":"メーカー",
            "displacement":"排気量",
            "modelname":"車種名",
            "price":"値段",
            "explanation":"商品説明",
            "modelyear":"年式",
            "mileage":"走行距離",
            "number":"ナンバー",
            "documents":"書類",
            "vehicleinspection":"車検",
            "vehicleinspectiondate":"車検期限",
            "condition":"状態",
            "prefectures":"発送元"
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelname'].queryset = MotorcycleModel.objects.none()
        current_year = datetime.now().year
        years = [(year,str(year)) for year in range(1950,current_year+1)]
        self.fields['modelyear'] = forms.ChoiceField(choices=years)

        # 車種などで絞り込んであるデータを表示
        if 'maker' in self.data and 'displacement' in self.data:
            maker = self.data.get('maker')
            displacement = self.data.get('displacement')
            self.fields['modelname'].queryset = MotorcycleModel.objects.filter(maker=maker, displacement=displacement)
            
    def save(self,commit=True):
        instance = super().save(commit=False)
        if instance.modelname:
            instance.type = instance.modelname.type
        if commit:
            instance.save()
        return instance



class CImageForm(forms.ModelForm):
    class Meta:
        model = CImageModel
        fields = ["files"]
        # 出品時なぜかformとして渡していない主キーとする外部キーの部分の必須エラーが出るので除外明示(modelを指定しているので通常は外部キーを必須にしなくてよい)
        exclude = ('testcar',)

class CInfoForm(forms.ModelForm):
    class Meta:
        model = CInfoModel
        fields = ["maker","modelname","price","explanation","modelyear","mission","color","mileage","number","vehicleinspection","condition","prefectures"]
        labels = {
            "maker":"メーカー",
            "modelname":"車種名",
            "price":"値段",
            "explanation":"商品説明",
            "modelyear":"年式",
            "mission":"ミッション",
            "color":"色",
            "mileage":"走行距離",
            "number":"ナンバー",
            "vehicleinspection":"車検",
            "condition":"状態",
            "prefectures":"発送元"
            }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        current_year = datetime.now().year
        years = [(year,str(year)) for year in range(1950,current_year+1)]
        self.fields['modelyear'] = forms.ChoiceField(choices=years)
        self.fields['modelname'].queryset = CarModel.objects.none()
        
        if 'maker' in self.data:
            maker = self.data.get('maker')
            self.fields['modelname'].queryset = CarModel.objects.filter(maker=maker)
        elif self.instance and self.instance.maker:
            self.fields['modelname'].queryset = CarModel.objects.filter(maker=self.instance.maker)
            
    def save(self,commit=True):
        instance = super().save(commit=False)
        if instance.modelname:
            instance.type = instance.modelname.type
        if commit:
            instance.save()
        return instance
    
class BImageForm(forms.ModelForm):
    class Meta:
        model = BImageModel
        fields = ["files"]
        # 出品時なぜかformとして渡していない主キーとする外部キーの部分の必須エラーが出るので除外明示(modelを指定しているので通常は外部キーを必須にしなくてよい)
        exclude = ('testbike',)
    
class BInfoForm(forms.ModelForm):
    class Meta:
        model = BInfoModel
        fields = ["maker","modelname","price","explanation","condition","prefectures"]
        labels = {
            "maker":"メーカー",
            "modelname":"車種名",
            "price":"値段",
            "explanation":"商品説明",
            "condition":"状態",
            "prefectures":"発送元"
            }

    
# class bikeForm(forms.ModelForm):
#     class Meta:
#         model = bikeshuppin
#         fields = ["maker","modelname","price","explanation","condition","prefectures"]
#         # labels  = [
#         #     'maker':'メーカー',
#         #     'modelname':'車種名',
#         #     'price':'値段',
#         #     'explanation':'詳細説明',
#         #     'mileage':'走行距離',
#         #     'modelyear':'年式',
#         #     'number':'ナンバー',
#         #     'vehicleinspection':'車検',
#         #     'condition':'状態',
#         #     'prefectures':'発送元',
#         # ]
        
# class bikeImageForm(forms.ModelForm):
#     class Meta:
#         model = bikeImage
#         fields = ["image"]
        
# bikeImageFormSet = inlineformset_factory(
#     bikeshuppin,
#     bikeImage,
#     form=bikeImageForm,
#     extra=1)
