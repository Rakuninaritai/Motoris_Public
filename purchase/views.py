from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Purchase_car,Purchase_mc,month_choises,year_choises ,Purchase_by
from shuppin.models import MCInfoModel,MCImageModel,CInfoModel,CImageModel,BInfoModel,BImageModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Payment_method,Purchase_after
import datetime
from datetime import timedelta

# Create your views here.

# 関数(どのモビリティのモデルか判断する関数)
def Product_Models(Products,product_id):
  if Products=="CInfoModel":
      product=get_object_or_404(CInfoModel,id=product_id)
      return product
  elif Products=="BInfoModel":
      product=get_object_or_404(BInfoModel,id=product_id)
      return product
  elif Products=="MCInfoModel":
      product=get_object_or_404(MCInfoModel,id=product_id)
      return product
  else:
    pass
  
# 関数(どの購入モビリティか判断する関数)
def Puechase_Models(Purchases,purchase_id):
  if Purchases=="Purchase_car":
      purchase=get_object_or_404(Purchase_car,id=purchase_id)
      return purchase
  elif Purchases=="Purchase_by":
      purchase=get_object_or_404(Purchase_by,id=purchase_id)
      return purchase
      
  elif Purchases=="Purchase_mc":
      purchase=get_object_or_404(Purchase_mc,id=purchase_id)
      return purchase
  else:
    # return redirect('/')
    pass
  
# 関数(どの購入モビリティか判断する関数)(Productモデルの名前から)
def Puechase_Models_Product(Product):
  if Product=="CInfoModel":
      purchase=Purchase_car()
      return purchase
  elif Product=="BInfoModel":
      purchase=Purchase_by()
      return purchase
      pass
  elif Product=="MCInfoModel":
      purchase=Purchase_mc()
      return purchase
  else:
    pass

# どの画像がどのtitleか(car)
carimti={
  31:"取得した書類の画像",32:"封筒の画像",33:"受け取った封筒の画像",34:"取得した書類の画像",35:"取得した車検証の画像",36:"取得した車庫証明などの画像",37:"発送する車の画像",38:"受け取った車の画像",404:"作業なし"
  }


# どの画像がどのtitleか(by)
byimti={
  31:"防犯登録抹消の画像",32:"譲渡証明書の画像",33:"送る封筒の画像",34:"受け取った封筒の画像",35:"発送する自転車の画像",36:"受け取った自転車の画像",37:"防犯登録した画像",404:"作業なし"
  }

#どの画像がどのtitleか(mc)
mcimti={
  31:"取得した書類の画像",32:"送る封筒の画像",33:"受け取った封筒の画像",34:"名義変更の書類画像",35:"ナンバーなどの画像",36:"発送するバイクの画像",37:"受け取ったバイクの画像",404:"作業なし"
}

# 購入ページ(決済ページ)
class PurchaseView(LoginRequiredMixin, View):
  # postでもgetでも使う部分
  def douteki(self,):
    # 現時刻から三日後
    kigen=datetime.date.today()+timedelta(days=3)
    return kigen
  
  def get(self,request,product_id,products):
    
    # どのモビリティか判断してその商品を持ってくる
    product=Product_Models(products,product_id)
    # ペイメントメゾットformはどのmodelsに指定するか書いていないのでそれをproductのmodelから割り出す
    # 引数はproductのモデル名
    ins=Puechase_Models_Product(product.__class__.__name__)
    # その商品が出品中でない場合(買われている場合)にこのurlにアクセスしたら
    if product.soldflag ==True:
      # topに飛ぶ
      return redirect('/')
    form=Payment_method(instance=ins)
    # 期限変わるもの呼び出し
    kigen=self.douteki()
    
    return render(request,'purchase/payment.html',{'form':form,'product':product,'kigen':kigen})
  
  def post(self,request,product_id,products):
    # どのモビリティか判断してその商品を持ってくる
    product=Product_Models(products,product_id)
    # ペイメントメゾットformはどのmodelsに指定するか書いていないのでそれをproductのmodelから割り出す
    # 引数はproductのモデル名
    ins=Puechase_Models_Product(product.__class__.__name__)
    form=Payment_method(request.POST,instance=ins)
    
    if form.is_valid():
      # formのインスタンスを作成して、保存前に追加情報を設定
      # formのインスタンス作成
      form_instance=form.save(commit=False)
      form_instance.user=request.user
      form_instance.product=product
      form_instance.save()
      
      # 商品をsoldにする
      product.soldflag=True
      # 商品の状態を出品中から購入完了にする
      product.status=31
      product.save()
      
      # 購入後に購入完了にリダイレクト
      # 保存したばっかのpurchaseのidを取得
      purchaseid=form_instance.id
      mode=ins.__class__.__name__
      return redirect('purchase_clear', mode,purchaseid) 
    
    else:
      # 日付呼び出し
      kigen=self.douteki()
      return render(request,'purchase/payment.html',{'form':form,'product':product,'kigen':kigen,})

  
# 購入完了ページ(決済完了ページ)
class Purchase_clearView(LoginRequiredMixin,View):
  def get(self,request,purchase,purchase_id):
    purchase=Puechase_Models(purchase,purchase_id)
    purchase_product=purchase.product
    # まだ販売中なら
    if purchase_product.soldflag==False:
      # topに飛ぶ
      return redirect('/')
    # 製品の画像(画像の外部キーはそのCInfoで名前にimagesをしてるのでそれで取れるかつ最初の画像)
    productimg=purchase.product.images.first()
    
    return render(request ,'purchase/payment_clear.html',{'purchase':purchase,'product':purchase_product,'productimg':productimg})


# 購入後取引ページ
class Purchase_afterview(LoginRequiredMixin,View):
  def Purchase_kaku(self,request,purchase,purchase_id):
    purchase=Puechase_Models(purchase,purchase_id)
    # purchaseがあるってことは購入完了してるからいつものifかかない
    product_user=purchase.product.user
    product_status=purchase.product.status
    zokusei=None
    ziclear=None
    nkm=[]
    # 購入者の場合
    if purchase.user==request.user:
      zokusei='kounyu'
      # さらに車の場合
      if purchase.__class__.__name__=='Purchase_car':
        print(f"product_status: {product_status}")
        nkm=[
          {"id":"1","title":"書類受け取り","text":"出品者から書類を受け取ってください。","aite":"完了","bt":"disabled","acti":"","ziti":[carimti[33]],"ziim":[""],"aiti":[carimti[31],carimti[32]],"aiim":["",""],"aizi":"","zizi":""},
          {"id":"2","title":"書類準備","text":"印鑑証明(普通車)、住民票(軽自動車)を用意してください。\n-必要書類\n・印鑑証明(普通車)、住民票(軽自動車)","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[carimti[34]],"ziim":[""],"aiti":[carimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"3","title":"車検証取得","text":"1の書類を陸運局に提出し、新しい車検証を取得してください。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[carimti[35]],"ziim":[""],"aiti":[carimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"4","title":"名義変更","text":"車庫証明を警察署で取得(普通車のみ)と自賠責を保険会社で名義変更してください。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[carimti[36]],"ziim":[""],"aiti":[carimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"5","title":"車受け取り","text":"車を受け取れます!\n良いカーライフを!","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[carimti[38]],"ziim":[""],"aiti":[carimti[37]],"aiim":[""],"aizi":"","zizi":""},
        ]
        if product_status==31:
          nkm[0]["aite"]="書類準備中"
          nkm[0]["acti"]="active"
          
        if product_status==32:
          nkm[0]["aite"]="書類郵送準備中"
          nkm[0]["acti"]="active"
          nkm[0]["aiim"][0]=purchase.im31.url
          
        if product_status==33:
          nkm[0]["aite"]="書類郵送中"
          nkm[0]["acti"]="active" 
          nkm[0]["bt"]=""
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
          
        
        if product_status>=34 or product_status==4:
          nkm[0]["aite"]="完了"
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
          nkm[0]["ziim"][0]=purchase.im33.url
          
        if product_status==34:
          nkm[1]["acti"]="active"
          nkm[1]["bt"]=""
          nkm[1]["aite"]="購入者完了待ち"
          
        if product_status>=35 or product_status==4:
          nkm[1]["aite"]="完了"
          nkm[1]["ziim"][0]=purchase.im34.url
          
        if product_status==35:
          nkm[2]["acti"]="active"
          nkm[2]["bt"]=""
          nkm[2]["aite"]="購入者完了待ち"
        
        if product_status>=36 or product_status==4:
          nkm[2]["aite"]="完了"
          nkm[2]["ziim"][0]=purchase.im35.url
          
          
        if product_status==36:
          nkm[3]["acti"]="active"
          nkm[3]["bt"]=""
          nkm[3]["aite"]="購入者完了待ち"
        
        if product_status>=37 or product_status==4:
          nkm[3]["aite"]="完了"
          nkm[3]["ziim"][0]=purchase.im36.url
          
        
        if product_status==37:
          nkm[4]["acti"]="active"
          nkm[4]["aite"]="車発送準備中"
        
        if product_status==38:
          nkm[4]["acti"]="active"
          nkm[4]["bt"]=""
          nkm[4]["aite"]="車発送中"
          nkm[4]["aiim"][0]=purchase.im37.url
          
        if product_status==4:
          nkm[4]["acti"]="active"
          nkm[4]["aite"]="完了"
          nkm[4]["aiim"][0]=purchase.im37.url
          nkm[4]["ziim"][0]=purchase.im38.url
          ziclear=True
          
        # 画像とタイトルの組み合わせを一つにまとめて(aiziとziziに)for文で一緒に回せるようにする
        for item in nkm:
          item["aizi"]=zip(item["aiti"],item["aiim"])
          item["zizi"]=zip(item["ziti"],item["ziim"])
            
          
          
          
      # 自転車の場合
      elif purchase.__class__.__name__=='Purchase_by':
        nkm=[
          {"id":"1","title":"書類受け取り","text":"出品者から書類を受け取ってください。(防犯登録抹消後、書類準備になります。)","aite":"完了","bt":"disabled","acti":"","ziti":[byimti[34]],"ziim":[""],"aiti":[byimti[31],byimti[32],byimti[33]],"aiim":["","",""],"aizi":"","zizi":""},
          {"id":"2","title":"自転車受け取り","text":"出品者から自転車を受け取ってください。","aite":"前項目未完了","bt":"disabled","acti":"","aite":"完了","bt":"disabled","acti":"","ziti":[byimti[36]],"ziim":[""],"aiti":[byimti[35]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"3","title":"防犯登録","text":"自転車販売店で防犯登録をしてください。\n-必要なもの\n・1で受け取った書類(譲渡証明書など)、身分証、自転車","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[byimti[37]],"ziim":[""],"aiti":[byimti[404]],"aiim":[""],"aizi":"","zizi":""},
        ]
        if product_status==31:
          nkm[0]["aite"]="防犯登録抹消中"
          nkm[0]["acti"]="active"
        if product_status==32:
          nkm[0]["aite"]="書類準備中"
          nkm[0]["acti"]="active"
          nkm[0]["aiim"][0]=purchase.im31.url
          
        if product_status==33:
          nkm[0]["aite"]="書類郵送準備中"
          nkm[0]["acti"]="active" 
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
          
        if product_status==34:
          nkm[0]["acti"]="active"
          nkm[0]["bt"]=""
          nkm[0]["aite"]="書類輸送中"
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
          nkm[0]["aiim"][2]=purchase.im33.url
        
        if product_status>=35 or product_status==4:
          nkm[0]["aite"]="完了"
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
          nkm[0]["aiim"][2]=purchase.im33.url
          nkm[0]["ziim"][0]=purchase.im34.url
          
        if product_status==35:
          nkm[1]["acti"]="active"
          nkm[1]["aite"]="自転車発送準備中"
          
        if product_status==36:
          nkm[1]["acti"]="active"
          nkm[1]["aite"]="自転車発送中"
          nkm[1]["bt"]=""
          nkm[1]["aiim"][0]=purchase.im35.url
          
        if product_status>=37 or product_status==4:
          nkm[1]["aite"]="完了"
          nkm[1]["aiim"][0]=purchase.im35.url
          nkm[1]["ziim"][0]=purchase.im36.url
          
          
        if product_status==37:
          nkm[2]["acti"]="active"
          nkm[2]["aite"]="完了"
          nkm[2]["bt"]=""
          
        if product_status==4:
          nkm[2]["aite"]="完了"
          nkm[2]["acti"]="active"
          nkm[2]["ziim"][0]=purchase.im37.url
          ziclear=True
          
        
        # 画像とタイトルの組み合わせを一つにまとめて(aiziとziziに)for文で一緒に回せるようにする
        for item in nkm:
          item["aizi"]=zip(item["aiti"],item["aiim"])
          item["zizi"]=zip(item["ziti"],item["ziim"])
          
      # バイクの場合
      elif purchase.__class__.__name__=='Purchase_mc':
        nkm=[
          {"id":"1","title":"書類受け取り","text":"出品者から書類を受け取ってください。\n-受け取る書類\n・譲渡証明書、廃車証明書、自賠責書類","aite":"完了","bt":"disabled","acti":"","ziti":[mcimti[33]],"ziim":[""],"aiti":[mcimti[31],mcimti[32]],"aiim":["",""],"aizi":"","zizi":""},
          # 発送したら画像が出てほしい
          {"id":"2","title":"名義変更","text":"市役所(原付)、陸運局(軽二輪、小型二輪)で名義変更を行ってください。\n-持参物:\n・1で受け取った書類、身分証明書、印鑑","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[mcimti[34]],"ziim":[""],"aiti":[mcimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"3","title":"ナンバーなどの取得","text":"新しいナンバーと登録証を受け取ってください。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[mcimti[35]],"ziim":[""],"aiti":[mcimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"4","title":"バイク受け取り","text":"バイクを受け取れます!\n良いバイクライフを!","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[mcimti[37]],"ziim":[""],"aiti":[mcimti[36]],"aiim":[""],"aizi":"","zizi":""},
        ]
        if product_status==31:
          nkm[0]["aite"]="書類準備中"
          nkm[0]["acti"]="active"
        if product_status==32:
          nkm[0]["aite"]="書類郵送準備中"
          nkm[0]["acti"]="active" 
          nkm[0]["aiim"][0]=purchase.im31.url
          
        if product_status==33:
          nkm[0]["aite"]="書類郵送中"
          nkm[0]["acti"]="active" 
          nkm[0]["bt"]=""
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
        
        if product_status>=34 or product_status==4:
          nkm[0]["aite"]="完了"
          nkm[0]["aiim"][0]=purchase.im31.url
          nkm[0]["aiim"][1]=purchase.im32.url
          nkm[0]["ziim"][0]=purchase.im33.url
          
          
        if product_status==34:
          nkm[1]["acti"]="active"
          nkm[1]["bt"]=""
          nkm[1]["aite"]="購入者完了待ち"
          
        if product_status>=35 or product_status==4:
          nkm[1]["aite"]="完了"
          nkm[1]["ziim"][0]=purchase.im34.url
          

        if product_status==35:
          nkm[2]["acti"]="active"
          nkm[2]["bt"]=""
          nkm[2]["aite"]="購入者完了待ち"
          
        if product_status>=36 or product_status==4:
          nkm[2]["aite"]="完了"
          nkm[2]["ziim"][0]=purchase.im35.url
        
        if product_status==36:
          nkm[3]["acti"]="active"
          nkm[3]["aite"]="バイク発送準備中"
          
        if product_status==37:
          nkm[3]["acti"]="active"
          nkm[3]["aite"]="バイク発送中"
          nkm[3]["bt"]=""
          nkm[3]["aiim"][0]=purchase.im36.url
          
          
        if product_status==4:
          nkm[3]["aite"]="完了"
          nkm[3]["acti"]="active"
          nkm[3]["aiim"][0]=purchase.im36.url
          nkm[3]["ziim"][0]=purchase.im37.url
          ziclear=True
          
        # 画像とタイトルの組み合わせを一つにまとめて(aiziとziziに)for文で一緒に回せるようにする
        for item in nkm:
          item["aizi"]=zip(item["aiti"],item["aiim"])
          item["zizi"]=zip(item["ziti"],item["ziim"])
      
    #出品者の場合
    elif request.user==product_user:
      zokusei='shuppin'
      # さらに車の場合
      if purchase.__class__.__name__=='Purchase_car':
        nkm=[
          {"id":"1","title":"書類準備","text":"必要な書類を準備してください。\n-必要書類:\n・車検証、自賠責証明、販売店書類(所有県権解除が必要な場合)、印鑑証明","aite":"完了","bt":"disabled","acti":"","ziti":[carimti[31]],"ziim":[""],"aiti":[carimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"2","title":"書類引き渡し","text":"1で準備した書類を購入者に郵送してください。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[carimti[32]],"ziim":[""],"aiti":[carimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"3","title":"車引き渡し","text":"購入者が名義変更完了し車庫証明などを取得したのち、車を渡してください。\nご利用ありがとうございました。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[carimti[37]],"ziim":[""],"aiti":[carimti[33],carimti[34],carimti[35],carimti[36],carimti[38]],"aiim":["","","","",""],"aizi":"","zizi":""}
        ]
        
        if product_status==31:
          nkm[0]["bt"]=""
          nkm[0]["aite"]="出品者完了待ち"
          nkm[0]["acti"]="active"
        
        if product_status>=32 or product_status==4:
          nkm[0]["aite"]="完了"
          nkm[0]["ziim"][0]=purchase.im31.url
          
        if product_status==32:
          nkm[1]["aite"]="出品者完了待ち"
          nkm[1]["acti"]="active" 
          nkm[1]["bt"]=""
        
        if product_status>=33 or product_status==4:
          nkm[1]["aite"]="完了"
          nkm[1]["ziim"][0]=purchase.im32.url
        
        if product_status==33:
          nkm[2]["aite"]="書類郵送確認中"
          nkm[2]["acti"]="active" 
        if product_status==34:
          nkm[2]["aite"]="書類準備中"
          nkm[2]["acti"]="active" 
          nkm[2]["aiim"][0]=purchase.im33.url
          
        if product_status==35:
          nkm[2]["aite"]="車検証取得中"
          nkm[2]["acti"]="active" 
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
        
        if product_status==36:
          nkm[2]["aite"]="名義変更中"
          nkm[2]["acti"]="active"
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
          nkm[2]["aiim"][2]=purchase.im35.url
          
        if product_status==37:
          nkm[2]["aite"]="出品者完了待ち"
          nkm[2]["acti"]="active" 
          nkm[2]["bt"]=""
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
          nkm[2]["aiim"][2]=purchase.im35.url
          nkm[2]["aiim"][3]=purchase.im36.url
        
        # めんどいから一度画像確定
        if product_status>=38 or product_status==4:
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
          nkm[2]["aiim"][2]=purchase.im35.url
          nkm[2]["aiim"][3]=purchase.im36.url
          nkm[2]["ziim"][0]=purchase.im37.url
          ziclear=True
          
        if product_status==38:
          nkm[2]["aite"]="受け取り中"
          nkm[2]["acti"]="active" 
          
        if product_status==4:
          nkm[2]["aite"]="完了"
          nkm[2]["acti"]="active"
          nkm[2]["aiim"][4]=purchase.im38.url
        
        # 画像とタイトルの組み合わせを一つにまとめて(aiziとziziに)for文で一緒に回せるようにする
        for item in nkm:
          item["aizi"]=zip(item["aiti"],item["aiim"])
          item["zizi"]=zip(item["ziti"],item["ziim"])
          
      # 自転車の場合
      elif purchase.__class__.__name__=='Purchase_by':
        nkm=[
          {"id":"1","title":"防犯登録抹消","text":"防犯登録を自転車販売店などで抹消してください。\n-必要なもの\n・自転車、身分証、防犯登録カード(防犯登録時に受取済)","aite":"完了","bt":"disabled","acti":"","ziti":[byimti[31]],"ziim":[""],"aiti":[byimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"2","title":"譲渡証明書作成","text":"必要事項を記載し譲渡証明書を作成してください。\n-必要事項\n・譲渡人(出品者)情報、自転車情報","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[byimti[32]],"ziim":[""],"aiti":[byimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"3","title":"書類郵送","text":"2で作成した譲渡証明書を購入者に郵送してください。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[byimti[33]],"ziim":[""],"aiti":[byimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"4","title":"自転車引き渡し","text":"書類の受け取り確認後、自転車を渡してください。\nご利用ありがとうございました。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[byimti[35]],"ziim":[""],"aiti":[byimti[34],byimti[36],byimti[37]],"aiim":["","",""],"aizi":"","zizi":""},
        ]
        if product_status==31:
          nkm[0]["bt"]=""
          nkm[0]["aite"]="出品者完了待ち"
          nkm[0]["acti"]="active"
          
        if product_status>=32 or product_status==4:
          nkm[0]["ziim"][0]=purchase.im31.url
          nkm[0]["aite"]="完了"
        
        if product_status==32:
          nkm[1]["aite"]="出品者完了待ち"
          nkm[1]["acti"]="active" 
          nkm[1]["bt"]=""
          
        if product_status>=33 or product_status==4:
          nkm[1]["ziim"][0]=purchase.im32.url
          nkm[1]["aite"]="完了"
          
        if product_status==33:
          nkm[2]["aite"]="出品者完了待ち"
          nkm[2]["acti"]="active" 
          nkm[2]["bt"]=""
        
        if product_status>=34 or product_status==4:
          nkm[2]["ziim"][0]=purchase.im33.url
          nkm[2]["aite"]="完了"
          
        if product_status==34:
          nkm[3]["aite"]="書類郵送確認中"
          nkm[3]["acti"]="active" 
          
        if product_status==35:
          nkm[3]["aite"]="出品者完了待ち"
          nkm[3]["acti"]="active" 
          nkm[3]["bt"]=""
          nkm[3]["aiim"][0]=purchase.im34.url
        
        if product_status==36:
          nkm[3]["aite"]="受け取り中"
          nkm[3]["acti"]="active" 
          nkm[3]["aiim"][0]=purchase.im34.url
          nkm[3]["ziim"][0]=purchase.im35.url
          ziclear=True
          
          
        if product_status==37:
          nkm[3]["aite"]="防犯登録中"
          nkm[3]["acti"]="active" 
          nkm[3]["aiim"][0]=purchase.im34.url
          nkm[3]["ziim"][0]=purchase.im35.url 
          nkm[3]["aiim"][1]=purchase.im36.url
        
          
          
        if product_status==4:
          nkm[3]["acti"]="active"
          nkm[3]["aite"]="完了"
          nkm[3]["aiim"][0]=purchase.im34.url
          nkm[3]["ziim"][0]=purchase.im35.url 
          nkm[3]["aiim"][1]=purchase.im36.url
          nkm[3]["aiim"][2]=purchase.im37.url
          
        # 画像とタイトルの組み合わせを一つにまとめて(aiziとziziに)for文で一緒に回せるようにする
        for item in nkm:
          item["aizi"]=zip(item["aiti"],item["aiim"])
          item["zizi"]=zip(item["ziti"],item["ziim"])
          
      # バイクの場合
      elif purchase.__class__.__name__=='Purchase_mc':
        nkm=[
          {"id":"1","title":"廃車手続き","text":"市役所(原付)、陸運局(軽二輪、小型二輪)で廃車手続きを行ってください。\n-持参物\n・ナンバープレート、車検証等、身分証、印鑑","aite":"完了","bt":"disabled","acti":"","ziti":[mcimti[31]],"ziim":[""],"aiti":[mcimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"2","title":"書類引き渡し","text":"買主に書類を郵送してください。\n-渡す書類\n・譲渡証明書、廃車証明書、自賠責書類","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[mcimti[32]],"ziim":[""],"aiti":[mcimti[404]],"aiim":[""],"aizi":"","zizi":""},
          {"id":"3","title":"バイク引き渡し","text":"買主がナンバープレート取得後、バイクを渡してください。\nご利用ありがとうございました。","aite":"前項目未完了","bt":"disabled","acti":"","ziti":[mcimti[36]],"ziim":[""],"aiti":[mcimti[33],mcimti[34],mcimti[35],mcimti[37]],"aiim":["","","",""],"aizi":"","zizi":""},
        ]
        if product_status==31:
          nkm[0]["bt"]=""
          nkm[0]["aite"]="出品者完了待ち"
          nkm[0]["acti"]="active"
        
        if product_status>=32 or product_status==4:
          nkm[0]["ziim"][0]=purchase.im31.url
          nkm[0]["aite"]="完了"
          
        if product_status==32:
          nkm[1]["aite"]="出品者完了待ち"
          nkm[1]["acti"]="active" 
          nkm[1]["bt"]=""
          
        if product_status>=33 or product_status==4:
          nkm[1]["ziim"][0]=purchase.im32.url
          nkm[1]["aite"]="完了"
          
        if product_status==33:
          nkm[2]["aite"]="書類郵送確認中"
          nkm[2]["acti"]="active" 
          
        if product_status==34:
          nkm[2]["aite"]="名義変更中"
          nkm[2]["acti"]="active" 
          nkm[2]["aiim"][0]=purchase.im33.url
        if product_status==35:
          nkm[2]["aite"]="ナンバーなど取得中"
          nkm[2]["acti"]="active" 
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
          
        
        if product_status==36:
          nkm[2]["aite"]="出品者完了待ち"
          nkm[2]["acti"]="active" 
          nkm[2]["bt"]=""
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
          nkm[2]["aiim"][2]=purchase.im35.url
          
        if product_status>=37 or product_status==4:
          nkm[2]["aite"]="完了"
          nkm[2]["aiim"][0]=purchase.im33.url
          nkm[2]["aiim"][1]=purchase.im34.url
          nkm[2]["aiim"][2]=purchase.im35.url
          nkm[2]["ziim"][0]=purchase.im36.url
        
        if product_status==37:
          nkm[2]["aite"]="受け取り中"
          nkm[2]["acti"]="active" 
          ziclear=True
          
        if product_status==4:
          nkm[2]["aite"]="完了"
          nkm[2]["acti"]="active"
          nkm[2]["aiim"][3]=purchase.im37.url
        
        # 画像とタイトルの組み合わせを一つにまとめて(aiziとziziに)for文で一緒に回せるようにする
        for item in nkm:
          item["aizi"]=zip(item["aiti"],item["aiim"])
          item["zizi"]=zip(item["ziti"],item["ziim"])
        
        
    # どちらでもない場合(出品者購入者どちらでもない場合はdefaultの[]とnoneを返す)
    return  purchase, zokusei, nkm,ziclear
  
  
  # このページはログインしている人しか入れない
  def get(self,request,purchase,purchase_id):
    purchase,zokusei,nkm,ziclear=self.Purchase_kaku(request,purchase,purchase_id)
    form = Purchase_after()
    zyoutai=purchase.product.status
    # 製品の画像(画像の外部キーはそのCInfoで名前にimagesをしてるのでそれで取れるかつ最初の画像)
    productimg=purchase.product.images.first()
    # nkmがないということは購入者でも出品者でもない
    if not nkm:
            return redirect('/')
    return render(request ,'purchase/afterbought.html',{'purchase':purchase,'product':purchase.product,'nkm':nkm,'zokusei':zokusei,'form':form,'zyoutai':zyoutai,'ziclear':ziclear,'productimg':productimg})
      
  def post(self,request,purchase,purchase_id):
    purchase,zokusei,nkm,ziclear=self.Purchase_kaku(request,purchase,purchase_id)
    if not nkm:
            return redirect('/')
    # product_user=purchase.product.user
    product=purchase.product
    product_status=purchase.product.status
    if request.method == "POST":
      form=Purchase_after(request.POST,request.FILES)
      if form.is_valid():
        Photo = form.cleaned_data['im']
        # さらに車の場合
        if purchase.__class__.__name__=='Purchase_car':
          if product_status==38:
            # 写真保存
            purchase.im38=Photo
            product_status=4
          else:
            # 写真保存、保存場所はステータス対応している
            field_name = f"im{product_status}"  # 'im31', 'im32', ... に対応
            # purchase.im31=Photoをしてる↓
            setattr(purchase, field_name, Photo)  
            product_status+=1
          
          # 変数を変えても値は変更されないので直に変えに行く。
          purchase.product.status=product_status
          purchase.save()
          product.save()
        # 自転車の場合
        elif purchase.__class__.__name__=='Purchase_by':
          if product_status==37:
            # 写真保存
            purchase.im37=Photo
            product_status=4
          else:
            # 写真保存、保存場所はステータス対応している
            field_name = f"im{product_status}"  # 'im31', 'im32', ... に対応
            # purchase.im31=Photoをしてる↓
            setattr(purchase, field_name, Photo) 
            product_status+=1
          
          # 変数を変えても値は変更されないので直に変えに行く。
          purchase.product.status=product_status
          purchase.save()
          product.save()
          
        # バイクの場合
        elif purchase.__class__.__name__=='Purchase_mc':
          if product_status==37:
            # 写真保存
            purchase.im37=Photo
            product_status=4
          else:
            # 写真保存、保存場所はステータス対応している
            field_name = f"im{product_status}"  # 'im31', 'im32', ... に対応
            # purchase.im31=Photoをしてる↓
            setattr(purchase, field_name, Photo) 
            product_status+=1
            
          # 変数を変えても値は変更されないので直に変えに行く。
          purchase.product.status=product_status
          purchase.save()
          product.save()
      
      return redirect('purchase_after',purchase.__class__.__name__,purchase.id)
          
       

    
    
    