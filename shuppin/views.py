from django.shortcuts import render,redirect,get_object_or_404
# from .forms import motorcycleForm,motorcycleImageFormSet,carForm,carImageFormSet,bikeForm,bikeImageFormSet
# from .models import motorcycleshuppin,carshuppin,bikeshuppin
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import MCImageModel,MotorcycleModel,CImageModel,CarModel,BImageModel,CInfoModel,MCInfoModel,BInfoModel
from django import forms
from .forms import MCImageForm,MCInfoForm,CImageForm,CInfoForm,BImageForm,BInfoForm
from django.views.generic import TemplateView,UpdateView
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.forms import inlineformset_factory
from django.contrib import messages
import base64
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class shuppinHtmlView(TemplateView):
    template_name = 'shuppin/shuppin.html'
    
class befourshuppinHtmlView(TemplateView):
    template_name = 'shuppin/befourshuppin.html'

# この下のdefはログインしていないと開かない(出品はユーザー登録しないとエラーになる)
@login_required
def motorcycleuploadfunc(request):
    EXTRA = 16  # アップロード可能な画像の数
    TestModelFormSet = forms.modelformset_factory(MCImageModel, form=MCImageForm, extra=EXTRA)
    formset = TestModelFormSet(request.POST or None, request.FILES or None, queryset=MCImageModel.objects.none())
    
    if request.method == 'POST':
        motorcycle_form = MCInfoForm(request.POST)
        
        if motorcycle_form.is_valid() and formset.is_valid():
            request.session['form_data'] = request.POST
            # セッションに画像データを保存
            image_data = []
            for form in formset:
                if form.cleaned_data.get('files'):
                    file = form.cleaned_data['files']
                    encoded_image = base64.b64encode(file.read()).decode('utf-8')
                    image_data.append(f"data:{file.content_type};base64,{encoded_image}")
            request.session['image_data'] = image_data
            return redirect('mcheck')          
        else:
            print(motorcycle_form.errors)
            print(formset.errors)

    else:
        motorcycle_form = MCInfoForm()
        formset = TestModelFormSet(queryset=MCImageModel.objects.none())

    context = {
        'motorcycle_form': motorcycle_form,
        'form': formset,
    }
    return render(request, 'shuppin/Motorcycleshuppin.html', context)

def submit_motorcycle(request):
    if request.method == 'POST':
        form_data = request.session.get('form_data', {})
        image_data = request.session.get('image_data', [])
        motorcycle_form = MCInfoForm(form_data)

        if motorcycle_form.is_valid():
            motorcycle_instance = motorcycle_form.save(commit=False)
            motorcycle_instance.user = request.user
            motorcycle_instance.save()
            for image_base64 in image_data:
                content = ContentFile(base64.b64decode(image_base64.split(',')[1]))
                image_model = MCImageModel(testmotorcycle=motorcycle_instance)
                image_model.files.save(f"{motorcycle_instance.id}_{datetime.now().timestamp()}.jpg", content)
            del request.session['form_data']
            del request.session['image_data']
            return redirect('top')  # 適切なリダイレクト先に変更してください

    return redirect('mcheck')

def mcheck(request):
    session_form = request.session.get('form_data',{})
    images = request.session.get('image_data',[])
    model_number = session_form.get('modelname')  # `modelname` が番号として保存されている
    if model_number:
        try:
            model = MotorcycleModel.objects.get(number=model_number)
            session_form['modelname'] = model.name  # 番号をモデル名に置き換え
        except MotorcycleModel.DoesNotExist:
            session_form['modelname'] = "不明なモデル"  # 該当しない場合

    context = {
        'motorcycle_form': MCInfoForm(session_form),
        'images': images,  # プレビュー用画像データ
    }
    return render(request, 'shuppin/mcheck.html', context)


def load_MCmodelnames(request):
    maker = request.GET.get('maker')
    displacement = request.GET.get('displacement')
    modelnames = MotorcycleModel.objects.filter(maker=maker, displacement=displacement)
    return JsonResponse(list(modelnames.values('id', 'name')), safe=False)
    
class motorcycleView(TemplateView):
   template_name = 'shuppin/motorcycleshuppin.html'


@login_required
def caruploadfunc(request):
    EXTRA = 16
    TestModelFormSet = forms.modelformset_factory(CImageModel,form=CImageForm,extra=EXTRA)
    formset = TestModelFormSet(request.POST or None,request.FILES or None,queryset=CImageModel.objects.none())
    
    if request.method == 'POST':
        car_form = CInfoForm(request.POST)
        
        if car_form.is_valid() and formset.is_valid():
            request.session['form_data'] = request.POST
            image_data =[]
            for form in formset:
                if form.cleaned_data.get('files'):
                    file = form.cleaned_data['files']
                    encoded_image = base64.b64encode(file.read()).decode('utf-8')
                    image_data.append(f"data:{file.content_type};base64,{encoded_image}")
            request.session['image_data'] = image_data
            return redirect('ccheck')
        else:
            print(car_form.errors)
            print(formset.errors)          

    else:
        car_form = CInfoForm()
        formset = TestModelFormSet(queryset=CImageModel.objects.none())
    
    context = {
        'car_form':car_form,
        'form':formset,
    }
    return render(request,'shuppin/carshuppin.html',context)

def submit_car(request):
    if request.method == 'POST':
        form_data = request.session.get('form_data',{})
        image_data = request.session.get('image_data',[])
        car_form = CInfoForm(form_data)
        
        if car_form.is_valid():
            car_instance = car_form.save(commit=False)
            car_instance.user = request.user
            car_instance.save()
            for image_base64 in image_data:
                content = ContentFile(base64.b64decode(image_base64.split(',')[1]))
                image_model = CImageModel(testcar=car_instance)
                image_model.files.save(f"{car_instance.id}_{datetime.now().timestamp()}.jpg",content)
            del request.session['form_data']
            del request.session['image_data']
            return redirect('top')
        
    return redirect('ccheck')

def ccheck(request):
    session_form = request.session.get('form_data',{})
    images = request.session.get('image_data',[])
    model_number = session_form.get('modelname')
    if model_number:
        try:
            model = CarModel.objects.get(number=model_number)
            session_form['modelname'] = model.name
        except CarModel.DoesNotExist:
            session_form['modelname'] = "不明なモデル"
    
    context = {
        'car_form':CInfoForm(session_form),
        'images':images,
    }
    return render(request,'shuppin/ccheck.html',context)

def load_Cmodelnames(request):
    maker = request.GET.get('maker')
    modelnames = CarModel.objects.filter(maker=maker)
    return JsonResponse(list(modelnames.values('id', 'name')), safe=False)
@login_required
def bikeuploadfunc(request):
    EXTRA = 16
    TestModelFormSet = forms.modelformset_factory(BImageModel,form=BImageForm,extra=EXTRA)
    formset = TestModelFormSet(request.POST or None,request.FILES or None,queryset=BImageModel.objects.none())
    
    if request.method == 'POST':
        bike_form = BInfoForm(request.POST)
        
        if bike_form.is_valid() and formset.is_valid():
            request.session['form_data'] = request.POST
            image_data =[]
            for form in formset:
                if form.cleaned_data.get('files'):
                    file = form.cleaned_data['files']
                    encoded_image = base64.b64encode(file.read()).decode('utf-8')
                    image_data.append(f"data:{file.content_type};base64,{encoded_image}")
            request.session['image_data'] = image_data
            return redirect('bcheck')
        else:
            print(bike_form.errors)
            print(formset.errors)
    
    else:
        bike_form = BInfoForm()
        formset = TestModelFormSet(queryset=BImageModel.objects.none())
        
    context = {
        'bike_form':bike_form,
        'form':formset,
    }
    return render(request,'shuppin/bikeshuppin.html',context)

def submit_bike(request):
    if request.method == 'POST':
        form_data = request.session.get('form_data',{})
        image_data = request.session.get('image_data',[])
        bike_form = BInfoForm(form_data)
        
        if bike_form.is_valid():
            bike_instance = bike_form.save(commit=False)
            bike_instance.user = request.user
            bike_instance.save()
            for image_base64 in image_data:
                content = ContentFile(base64.b64decode(image_base64.split(',')[1]))
                image_model = BImageModel(testbike=bike_instance)
                image_model.files.save(f"{bike_instance.id}_{datetime.now().timestamp()}.jpg",content)
            del request.session['form_data']
            del request.session['image_data']
            return redirect('top')
        
    return redirect('bcheck')

# 編集view
# 車編集
@login_required
def car_edit(request, pk):
    """
    ログインユーザー自身の車情報（CInfoModel）の編集ビュー
    """
    # カーモデルをurlから渡されたidとログインしているユーザーから引っ張ってくる
    car = get_object_or_404(CInfoModel, pk=pk, user=request.user)
    # CInfoModel に紐づく画像を扱う inline formset(親モデルinfoと子モデルimageのモデルを紐づけてform化)
    ImageFormSet = inlineformset_factory(
        CInfoModel, 
        CImageModel, 
        # 子モデルの定義
        form=CImageForm, 
        extra=16, 
        # ユーザーによる削除true
        can_delete=True,
        min_num=0,        # o枚でも許容(jsではじきます)
        validate_min=False # 上記の条件をバリデーションに反映
    )
    
    if request.method == 'POST':
        car_form = CInfoForm(request.POST, instance=car)
        formset = ImageFormSet(request.POST, request.FILES, instance=car)
        # 追加画像用のファイルを、input の name 属性に合わせて取得
        additional_images = request.FILES.getlist("additional_images")
        if car_form.is_valid() and formset.is_valid():
            car_form.save()
            formset.save()
            for f in additional_images:
                CImageModel.objects.create(testcar=car, files=f)
            messages.success(request,"商品の編集に成功しました!")
            # リダイレクト先は当該製品
            return redirect('shohin:shohin_car', car_id=car.pk)
    else:
        car_form = CInfoForm(instance=car)
        formset = ImageFormSet(instance=car)
        
        
    context = {
        'car_form': car_form,  # 車情報のメインフォーム
        'form': formset,       # 画像用のフォームセット（HTML側は既存のものを流用）
        'car': car,            # 必要に応じて編集対象の車情報をテンプレートで利用可能
        "edit":True,
    }
    return render(request, 'shuppin/carshuppin.html', context)


# 車削除
@login_required
def car_delete(request, pk):
    """
    ログインユーザー自身の車情報を削除するビュー
    """
    car = get_object_or_404(CInfoModel, pk=pk, user=request.user)
    
    if request.method == "POST":
        car.delete()
        messages.success(request, "商品が削除されました。")
        return redirect("top")  # 削除後のリダイレクト先
    
    # GET の場合は確認ページへリダイレクトまたは確認ダイアログを表示（ここでは簡単にリダイレクト）
    messages.error(request, "削除の確認が取れませんでした。")
    return redirect("carChange", pk=pk)

# バイク
@login_required
def mc_edit(request, pk):
    """
    ログインユーザー自身のバイク情報（MCInfoModel）の編集ビュー
    """
    # バイクモデルをurlから渡されたidとログインしているユーザーから引っ張ってくる
    mc = get_object_or_404(MCInfoModel, pk=pk, user=request.user)
    # MCInfoModel に紐づく画像を扱う inline formset(親モデルinfoと子モデルimageのモデルを紐づけてform化)
    ImageFormSet = inlineformset_factory(
        MCInfoModel, 
        MCImageModel, 
        # 子モデルの定義
        form=MCImageForm, 
        extra=16, 
        # ユーザーによる削除true
        can_delete=True,
        min_num=0,        # o枚でも許容(jsではじきます)
        validate_min=False # 上記の条件をバリデーションに反映
    )
    
    if request.method == 'POST':
        mc_form = MCInfoForm(request.POST, instance=mc)
        formset = ImageFormSet(request.POST, request.FILES, instance=mc)
        # 追加画像用のファイルを、input の name 属性に合わせて取得
        additional_images = request.FILES.getlist("additional_images")
        if mc_form.is_valid() and formset.is_valid():
            mc_form.save()
            formset.save()
            for f in additional_images:
                MCImageModel.objects.create(testmotorcycle=mc, files=f)
            messages.success(request,"商品の編集に成功しました!")
            # リダイレクト先は当該製品
            return redirect('shohin:shohin_motorBike', bike_id=mc.pk)
    else:
        mc_form = MCInfoForm(instance=mc)
        formset = ImageFormSet(instance=mc)
        
        
    context = {
        'motorcycle_form': mc_form,  # 車情報のメインフォーム
        'form': formset,       # 画像用のフォームセット（HTML側は既存のものを流用）
        'mc': mc,            # 必要に応じて編集対象の車情報をテンプレートで利用可能
        "edit":True,
    }
    return render(request, 'shuppin/motorcycleshuppin.html', context)

# バイク削除
@login_required
def mc_delete(request, pk):
    """
    ログインユーザー自身のバイク情報を削除するビュー
    """
    mc = get_object_or_404(MCInfoModel, pk=pk, user=request.user)
    
    if request.method == "POST":
        mc.delete()
        messages.success(request, "商品が削除されました。")
        return redirect("top")  # 削除後のリダイレクト先
    
    # GET の場合は確認ページへリダイレクトまたは確認ダイアログを表示（ここでは簡単にリダイレクト）
    messages.error(request, "削除の確認が取れませんでした。")
    return redirect("motorcycleChange", pk=pk)

# 自転車
@login_required
def by_edit(request, pk):
    """
    ログインユーザー自身の自転車情報（BInfoModel）の編集ビュー
    """
    # 自転車モデルをurlから渡されたidとログインしているユーザーから引っ張ってくる
    by = get_object_or_404(BInfoModel, pk=pk, user=request.user)
    # BInfoModel に紐づく画像を扱う inline formset(親モデルinfoと子モデルimageのモデルを紐づけてform化)
    ImageFormSet = inlineformset_factory(
        BInfoModel, 
        BImageModel, 
        # 子モデルの定義
        form=BImageForm, 
        extra=16, 
        # ユーザーによる削除true
        can_delete=True,
        min_num=0,        # o枚でも許容(jsではじきます)
        validate_min=False # 上記の条件をバリデーションに反映
    )
    
    if request.method == 'POST':
        by_form = BInfoForm(request.POST, instance=by)
        formset = ImageFormSet(request.POST, request.FILES, instance=by)
        # 追加画像用のファイルを、input の name 属性に合わせて取得
        additional_images = request.FILES.getlist("additional_images")
        if by_form.is_valid() and formset.is_valid():
            by_form.save()
            formset.save()
            for f in additional_images:
                BImageModel.objects.create(testbike=by, files=f)
            messages.success(request,"商品の編集に成功しました!")
            # リダイレクト先は当該製品
            return redirect('shohin:shohin_bike', bike_id=by.pk)
    else:
        by_form = BInfoForm(instance=by)
        formset = ImageFormSet(instance=by)
        
        
    context = {
        'bike_form': by_form,  # 車情報のメインフォーム
        'form': formset,       # 画像用のフォームセット（HTML側は既存のものを流用）
        'by': by,            # 必要に応じて編集対象の車情報をテンプレートで利用可能
        "edit":True,
    }
    return render(request, 'shuppin/bikeshuppin.html', context)

# 自転車削除
@login_required
def by_delete(request, pk):
    """
    ログインユーザー自身の自転車情報を削除するビュー
    """
    by = get_object_or_404(BInfoModel, pk=pk, user=request.user)
    
    if request.method == "POST":
        by.delete()
        messages.success(request, "商品が削除されました。")
        return redirect("top")  # 削除後のリダイレクト先
    
    # GET の場合は確認ページへリダイレクトまたは確認ダイアログを表示（ここでは簡単にリダイレクト）
    messages.error(request, "削除の確認が取れませんでした。")
    return redirect("bikeChange", pk=pk)

def bcheck(request):
    session_form = request.session.get('form_data',{})
    images = request.session.get('image_data',[])
    
    context = {
        'bike_form':BInfoForm(session_form),
        'images':images,
    }
    return render(request,'shuppin/bcheck.html',context)

# def uploadfunc(request):
#     EXTRA = 5
#     UploadModelFormSet = forms.modelformset_factory(TestModel, form=SingleUploadModelForm,extra=EXTRA)
#     formset = UploadModelFormSet(request.POST or None, files=request.FILES or None, queryset=TestModel.objects.none())
#     if request.method == 'POST': #画像が選択され，送信されたとき
#         formset.save() #データベースに保存
#     context = {
#         'form': formset,
#         'number_list': list(range(EXTRA)),
#         'total_number': EXTRA,
#     }
#     return render(request, 'shuppin/motorcycleshuppin.html', context)


#class carView(TemplateView):
#    template_name = 'shuppin/carshuppin.html'

#class bikeView(TemplateView):
#   template_name = 'shuppin/bikeshuppin.html'
    
    
# def create_car(request):
#     if request.method == "POST":
#         form = carForm(request.POST)
#         formset = carImageFormSet(request.POST,request.FILES)
        
        
#         if form.is_valid() and formset.is_valid():
#             car = form.save()
#             images = formset.save(commit=False)
#             for image in images:
#                 image.car = car
#                 image.save()
#             return redirect('afterbought')
    
#     else:
#         form =carForm()
#         formset = carImageFormSet()
    
#     return render(request,'shuppin/carshuppin.html',{'form':form,'formset':formset})



# def create_motorcycle(request):
#     if request.method == "POST":
#         form = motorcycleForm(request.POST)
#         formset = motorcycleImageFormSet(request.POST,request.FILES)
        
#         if form.is_valid() and formset.is_valid():
#             motorcycle = form.save()
#             images = formset.save(commit=False)
#             for image in images:
#                 image.motorcycle = motorcycle
#                 image.save()
#             return redirect('afterbought')
    
#     else:
#         form =motorcycleForm()
#         formset = motorcycleImageFormSet()
    
#     return render(request,'shuppin/motorcycleshuppin.html',{'form':form,'formset':formset})
    

    
# def create_bike(request):
#     if request.method == "POST":
#         form = bikeForm(request.POST)
#         formset = bikeImageFormSet(request.POST,request.FILES)
        
#         if form.is_valid() and formset.is_valid():
#             bike = form.save()
#             images = formset.save(commit=False)
#             for image in images:
#                 image.bike = bike
#                 image.save()
#             return redirect('afterbought')
    
#     else:
#         form =  bikeForm()
#         formset = bikeImageFormSet()
    
#     return render(request,'shuppin/bikeshuppin.html',{'form':form,'formset':formset})