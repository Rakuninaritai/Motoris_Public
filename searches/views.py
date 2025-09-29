from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from shuppin.models import MCInfoModel,MCImageModel,CInfoModel,CImageModel,BInfoModel,BImageModel
from shuppin.models import MotorcycleModel,CarModel#,BikeModel
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime 
from datetime import timedelta
from .forms import MCsf,Carsf,Bysf
from django.db.models import Q

# 検索ページ　logministかは要検討(ログインしなくてもあくせすできるのか)
class searchView(View):
    #db,formと表示をあらかじめ検索かけていない奴と総合が表示されるようにする
    #db
    
    # 総合dbデータ取得用
    def sougoudb(self,mcdb,cardb,bydb):
        # データを統一形式でまとめる
        sougoudb = []

        # for文現状表示のみクリア、検索で条件必要であれば別途追加(うそ、総合はtextだけだからok)
        for item in mcdb:
            sougoudb.append({
                'type': 'motorcycle',
                'id': item.id,  # IDを保持
                'maker': item.maker,
                'modelname': item.modelname.name,
                'price': item.price,
                'explanation':item.explanation,
                'condition': item.condition,
                'prefecture': item.prefectures,
                'sflag': item.soldflag,
                'image':item.images.first(),
            })

        for item in cardb:
            sougoudb.append({
                'type': 'car',
                'id': item.id,  # IDを保持
                'maker': item.maker,
                'modelname': item.modelname.name,
                'price': item.price,
                'explanation':item.explanation,
                'condition': item.condition,
                'prefecture': item.prefectures,
                'sflag': item.soldflag,
                'image':item.images.first(),
            })

        for item in bydb:
            sougoudb.append({
                'type': 'bike',
                'id': item.id,  # IDを保持
                'maker': item.maker,
                'modelname': item.modelname,
                'price': item.price,
                'explanation':item.explanation,
                'condition': item.condition,
                'prefecture': item.prefectures,
                'sflag': item.soldflag,
               'image':item.images.first(),
            })
        
        return sougoudb
    
     # データ取得
    def shutokuall(self):
        motorcycle_items = MCInfoModel.objects.all()
        car_items = CInfoModel.objects.all()
        bike_items = BInfoModel.objects.all()

        sougoudb=self.sougoudb(motorcycle_items,car_items,bike_items)

        # objects.all()でデータを取得
        cardb=CInfoModel.objects.all()
        mcdb=MCInfoModel.objects.all()
        bydb=BInfoModel.objects.all()
        # djangoはformレンダリング時デフォルトでidを付けるがfiel名が同じだとかぶるためautoをoff
        carf=Carsf(auto_id=False)
        mcf=MCsf(auto_id=False)
        byf=Bysf(auto_id=False)
        hyouzi="sougou"
        
        return sougoudb,cardb,mcdb,carf,mcf,byf,hyouzi,bydb
    
    def get(self,request,kensaku):
        # bydb追加してね!!!!!!!!!!!!!!!!!!!!!!!
        sougoudb,cardb,mcdb,carf,mcf,byf,hyouzi,bydb=self.shutokuall()
        # 絞り込み検索の項目
        kenko=""
        # 検索する文字列がないならそのまま表示(kensakuは""にしないとバーに*が表示されちゃう)
        if kensaku=="*":
            kensaku=""
        else:
            # モデルネームと説明に検索の文字列が入っていないか検索
            # __で外部キーの中のフィールドアクセス
            smdb=mcdb.filter(Q(modelname__name=kensaku)|Q(explanation=kensaku))
            scdb=cardb.filter(Q(modelname__name=kensaku)|Q(explanation=kensaku))
            sbdb=bydb.filter(Q(modelname=kensaku)|Q(explanation=kensaku))
            sougoudb=self.sougoudb(smdb,scdb,sbdb)
        
        return render(request ,'searches/search.html',{"kensaku":kensaku,"sougoudb":sougoudb,"cardb": cardb,"mcdb": mcdb,"bydb": bydb,"carf":carf,"mcf": mcf,"byf": byf,"hyouzi":hyouzi,'kenko':kenko})
    
    def post(self,request,kensaku):
        # めんどいんで検索は消します
        kensaku=""
        # 各dbのデフォルト値取得
        sougoudb,cardb,mcdb,carf,mcf,byf,hyouzi,bydb=self.shutokuall()
        # 各formでhiddnで送っているmobirityのタイプの取得
        mbt=request.POST.get("mbt")
        # 入力があった(検索させる)項目をappendさせる配列(どの絞り込みかけているか表示したいから)
        kenko=[]
        error=[]
        if mbt=="mc":
            # formを取得
            # 今回全項目が任意なためnull送信されてもNoneで受け止めエラーにならない
            mcf=MCsf(request.POST or None,auto_id=False)
            # 何を表示するか(デフォルトsougou)
            hyouzi="mc"
            
            # formバリデーション(上限値下限逆じゃないなど突破したら)
            if  mcf.is_valid():
                # それぞれバリデーション通った奴を取得
                maker = mcf.cleaned_data.get('maker')
                displacement = mcf.cleaned_data.get('displacement')
                modelname = mcf.cleaned_data.get('modelname')
                modelyear_min = mcf.cleaned_data.get('modelyear_min')
                modelyear_max = mcf.cleaned_data.get('modelyear_max')
                price_min = mcf.cleaned_data.get('price_min')
                price_max = mcf.cleaned_data.get('price_max')
                
                # それぞれnull時は''だったりnullだったりするけどifはそれぞれのデータ型に合わせて判断してくれる
                # その要素が入力(検索)されていれば
                if maker :
                    mcdb=mcdb.filter(maker=maker)
                    # 検索した項目を追加
                    kenko.append("メーカー")
                if displacement :
                    mcdb=mcdb.filter(displacement=displacement)
                    kenko.append("排気量")
                if modelname :
                    mcdb=mcdb.filter(modelname=modelname)
                    kenko.append("商品名")
                if modelyear_min :
                    # フィールド名__gteでその数値以上を絞り込める
                    # 年代とかは統一だから省略したかったけど結局どこのdb入れるかifラなあかんからなし
                    mcdb=mcdb.filter(modelyear__gte=modelyear_min)
                    kenko.append("年代(下限)")
                if modelyear_max :
                    # フィールド名__lteでその数値以下で絞り込める
                    mcdb=mcdb.filter(modelyear__lte=modelyear_max)
                    kenko.append("年代(上限)")
                if price_min :
                    # formのchoiceはvalue,labelでvalueはstr型だったんでintにする
                    mcdb=mcdb.filter(price__gte=int(price_min))
                    kenko.append("価格(下限)")
                if price_max:
                    mcdb=mcdb.filter(price__lte=int(price_max))
                    kenko.append("価格(上限)")
            else:
                mcdb=MCInfoModel.objects.none()
                # if price_min > price_max:
        if mbt=="car":
            carf=Carsf(request.POST or None,auto_id=False)
            hyouzi="car"
            
            if carf.is_valid():
                maker = carf.cleaned_data.get('maker')
                modelname = carf.cleaned_data.get('modelname')
                color = carf.cleaned_data.get('color')
                modelyear_min = carf.cleaned_data.get('modelyear_min')
                modelyear_max = carf.cleaned_data.get('modelyear_max')
                price_min = carf.cleaned_data.get('price_min')
                price_max = carf.cleaned_data.get('price_max')
                
                if maker :
                    cardb=cardb.filter(maker=maker)
                    kenko.append("メーカー")
                if modelname :
                    cardb=cardb.filter(modelname=modelname)
                    kenko.append("商品名")
                if color :
                    cardb=cardb.filter(color=color)
                    kenko.append("カラー")
                if modelyear_min :
                    cardb=cardb.filter(modelyear__gte=modelyear_min)
                    kenko.append("年代(下限)")
                if modelyear_max :
                    cardb=cardb.filter(modelyear__lte=modelyear_max)
                    kenko.append("年代(上限)")
                if price_min :
                    cardb=cardb.filter(price__gte=int(price_min))
                    kenko.append("価格(下限)")
                if price_max:
                    cardb=cardb.filter(price__lte=int(price_max))
                    kenko.append("価格(上限)")
                    
            else:
                cardb=CInfoModel.objects.none()
                
        if mbt=="by":
            byf=Bysf(request.POST or None,auto_id=False)
            hyouzi="by"
            
            if byf.is_valid():
                maker = byf.cleaned_data.get('maker')
                modelname = byf.cleaned_data.get('modelname')
                price_min = byf.cleaned_data.get('price_min')
                price_max = byf.cleaned_data.get('price_max')
                
                if maker :
                    bydb=bydb.filter(maker=maker)
                    kenko.append("メーカー")
                if modelname :
                    bydb=bydb.filter(modelname=modelname)
                    kenko.append("商品名")
                if price_min :
                    bydb=bydb.filter(price__gte=int(price_min))
                    kenko.append("価格(下限)")
                if price_max:
                    bydb=bydb.filter(price__lte=int(price_max))
                    kenko.append("価格(上限)")
                    
            else:
                bydb=BInfoModel.objects.none()
        
        sougoudb=self.sougoudb(mcdb,cardb,bydb)
            
        return render(request ,'searches/search.html',{"kensaku":kensaku,"sougoudb":sougoudb,"cardb": cardb,"mcdb": mcdb,"bydb": bydb,"carf":carf,"mcf": mcf,"byf": byf,"hyouzi":hyouzi,'kenko':kenko})