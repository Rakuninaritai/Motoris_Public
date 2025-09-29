from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from shuppin.models import MCInfoModel,MCImageModel,CInfoModel,CImageModel,BInfoModel,BImageModel
from shuppin.models import MotorcycleModel,CarModel#,BikeModel
from searches.views import searchView
from events.models import EventPost
from django.utils.timezone import now
from pprint import pprint
import random

class topView(View):
    def get(self,request):
        # データ取得(販売中の)
        mcdb=MCInfoModel.objects.filter(soldflag=False)
        cardb=CInfoModel.objects.filter(soldflag=False)
        bydb=BInfoModel.objects.filter(soldflag=False)
        # 全部まとめたものをおすすめとして最大28こにする(一周28個)
        osusume=searchView().sougoudb(mcdb,cardb,bydb)[:28]
        event = EventPost.objects.filter(event_date__gt=now()).prefetch_related('images')
        event = [random.choice(list(event))] if event.exists() else []
        # 各要素をmax28個にする
        mcdb=mcdb[:28]
        cardb=cardb[:28]
        bydb=bydb[:28]

        return render(request ,'top/top.html',{"mcdb":mcdb,"cardb":cardb,"bydb":bydb,"osusume":osusume,"event":event})
        
        
    
    # baseのformの処理を書いてる(baseのactionでここ指定してる)
    def post(self,request):
        # inputのtxtを取得、nullならから文字列を渡す。(なにも書かないとnone)
        try:
            kensakuka = request.POST.get('kensaku','')
            if kensakuka=='':
                # 何も書いてないとdb一覧表示
                return redirect('search', kensaku='*',)
            else:
                return redirect('search', kensaku=kensakuka)
        except:
            return redirect("top")



# カスタム404ビュー
def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

