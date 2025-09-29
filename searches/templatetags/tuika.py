#テンプレで扱えないものをこっちで扱う
# このフォルダ名じゃなきゃダメでアプリにないとダメ(テンプは離れててもloadファイル名で探しに来る)

# テンプレートライブラリーを呼ぶのにimport
from django import template
# htmlページで動かせるようにsafe
from django.utils.safestring import mark_safe
# url用
from django.urls import reverse


# 今回の処理を登録するテンプレートライブラリーを呼び出しregisterにin
register = template.Library()

# ↓でテンプレでも使える関数になる
@register.simple_tag

# dbを表示するためのhtmlを返す関数
def hyouzidb(db,name):
    html =""
    # 許容文字数(モデルネーム)(css側で制御)なので事実上無制限
    namelen=100
    # 許容文字数(説明)(css側で制御)事実上無制限
    textlen=100
    if (name=="sougoudb"):
        for item in db:
            # リストとして追加されていく
            # sougouは辞書で引っ張て来ているのでこの形式
            #製品が販売中以外なら売り切れと表示
            if item.get('sflag') == True :
                price="SOLD OUT!"
            else:
                price=f"￥{item.get('price'):,}"
            # mobirityを判断
            if item.get("type")=="motorcycle":
                mb="shohin:shohin_motorBike"
            elif item.get("type")=="car":
                mb="shohin:shohin_car"
            else:
                mb="shohin:shohin_bike"
            # urlを作成する
            url=reverse(mb,args=[item.get("id")])
            # モデルネームを取得
            modelname=item.get("modelname")
            # 商品名が8より大きい場合は以降…
            if len(modelname)>namelen:
                modelname=modelname[:namelen]+"…"
            # 説明を取得
            text=item.get("explanation")
            # 説明が13より大きい場合は
            if len(text)>textlen:
                text=text[:textlen]+"…"
            html+=f"""
                        <!--aタグはtypeかdb名でid番号と一緒にifを作る(idはtypeでも使えるように引っ張り済み)-->
                        <!-- カードのコンテナ -->
                        <div class="col zyoi">
                        <!-- 製品の状態 -->
                        <div class="zyoutai" hidden>{item.get('sflag')}</div>
                            <div class="card mb-5" style="max-width: 25rem">
                                <a href="{url}" class="text-dark text-decoration-none">
                                    <!-- カードの画像 -->
                                    <img class="card-img-top  shohin_img "  src="{item.get('image').files.url}" alt="{modelname}">
                                    <!-- カード本文 -->
                                    <div class="card-body">
                                        <!-- カードタイトル -->
                                        <h4 class="card-title mb-1 kaigyousanten">{modelname}</h4>
                                        <!-- 商品説明 -->
                                        <p class="card-text">商品説明</p>
                                        <p class="card-text kaigyousanten">{text}</p>
                                        <!-- 値段 -->
                                        <p class="card-text text-end text-danger price kaigyousanten">
                                            {price}
                                        </p>
                                    </div>
                                </a>
                            </div>
                        </a>
                    </div>
            
            """
    
    elif(name=="mcdb" or name=="cardb"):
        for item in db:
        # リストとして追加されていく
        # car,mc,byはdb引っ張り
        #製品が販売中以外なら売り切れと表示
        
            if item.soldflag==True:
                price="SOLD OUT!"
            else:
                price=f"￥{item.price:,}"
            # 商品名取得
            modelname=item.modelname.name
            # 商品名が8より大きい場合は以降…
            if len(modelname)>namelen:
                modelname=modelname[:namelen]+"…"
            # 説明取得
            text=item.explanation
            # 説明が13より大きい場合は
            if len(text)>textlen:
                text=text[:textlen]+"…"
            # url設定
            if name=="mcdb":
                url=reverse("shohin:shohin_motorBike",args=[item.id])
            else:
                url=reverse("shohin:shohin_car",args=[item.id])
            html+=f"""
                        <!--aタグはtypeかdb名でid番号と一緒にifを作る(idはtypeでも使えるように引っ張り済み)-->
                        <!-- カードのコンテナ -->
                        <div class="col zyoi">
                            <!-- 製品の状態 -->
                            <div class="zyoutai" hidden>{item.soldflag}</div>
                            <div class="card mb-5" style="max-width: 25rem">
                                <a href="{url}" class="text-dark text-decoration-none">
                                    <!-- カードの画像 -->
                                    <img class="card-img-top shohin_img"  src="{item.images.first().files.url}" alt="{modelname}">
                                    <!-- カード本文 -->
                                    <div class="card-body">
                                        <!-- カードタイトル -->
                                        <h4 class="card-title mb-1 kaigyousanten">{modelname}</h4>
                                        <!-- 商品説明 -->
                                        <p class="card-text">商品説明</p>
                                        <p class="card-text kaigyousanten">{text}</p>
                                        <!-- 値段 -->
                                        <p class="card-text text-end text-danger price kaigyousanten">
                                            {price}
                                        </p>
                                    </div>
                                </a>
                            </div>
                    </div>
            
            """
        
    # 商品名を引っ張って来れない奴は商品名外部キーではなくてちゃーフィールド
    else:
        for item in db:
        # リストとして追加されていく
        # car,mc,byはdb引っ張り
        #製品が販売中以外なら売り切れと表示
        
            if item.soldflag==True:
                price="SOLD OUT!"
            else:
                price=f"￥{item.price:,}"
                
            # 商品名取得
            modelname=item.modelname
            # 商品名が8より大きい場合は以降…
            if len(modelname)>namelen:
                modelname=modelname[:namelen]+"…"
            # 説明取得
            text=item.explanation
            # 説明が13より大きい場合は
            if len(text)>textlen:
                text=text[:textlen]+"…"
            url=reverse("shohin:shohin_bike",args=[item.id])
            html+=f"""
                        <!--aタグはtypeかdb名でid番号と一緒にifを作る(idはtypeでも使えるように引っ張り済み)-->
                        <!-- カードのコンテナ -->
                        <div class="col zyoi">
                        <!-- 製品の状態 -->
                        <div class="zyoutai" hidden>{item.soldflag}</div>
                        <div class="card mb-5" style="max-width: 25rem">
                            <a href="{url}" class="text-dark text-decoration-none">
                                <!-- カードの画像 -->
                                <img class="card-img-top shohin_img" src="{item.images.first().files.url}" alt="{modelname}">
                                <!-- カード本文 -->
                                <div class="card-body">
                                    <!-- カードタイトル -->
                                    <h4 class="card-title mb-1 kaigyousanten">{modelname}</h4>
                                    <!-- 商品説明 -->
                                    <p class="card-text">商品説明</p>
                                    <p class="card-text kaigyousanten">{text}</p>
                                    <!-- 値段 -->
                                    <p class="card-text text-end text-danger price kaigyousanten">
                                        {price}
                                    </p>
                                </div>
                            </a>
                        </div>
                    </div>
            
            """
    # htmlで動かせるsafe
    return mark_safe(html)