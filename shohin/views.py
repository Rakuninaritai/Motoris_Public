from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from shuppin.models import BInfoModel, BImageModel, CInfoModel, CImageModel, MCInfoModel, MCImageModel
from .models import Comment, Like
from .forms import CommentForm
from purchase.models import Purchase_by,Purchase_car,Purchase_mc

def shohin_bike_view(request, bike_id):
    bike = get_object_or_404(BInfoModel, id=bike_id)
    images = BImageModel.objects.filter(testbike=bike)
    comments = Comment.objects.filter(product_type='bike', product_id=bike_id).order_by('created_at')
    
    # いいねの合計数を取得
    like_count = Like.objects.filter(product_type='bike', product_id=bike_id).count()
    
    # ユーザーが既にいいねしているか確認
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            product_type='bike',
            product_id=bike_id
        ).exists()

    # 出品者かどうかをチェック
    is_seller = request.user.is_authenticated and request.user == bike.user
    
    # ボタンの状態を決定
    button_text = "購入"
    button_url = reverse('product_purchase', args=[bike.class_name, bike.id])
    
    # 購入後画面、商品編集画面はここにURLを！　osawa
    if bike.soldflag:
        button_text = "SOLDOUT"
        purchase=bike.by_product.get()
        button_url = reverse('purchase_after', args=["Purchase_by",purchase.id])    # または購入後ページへのURL
    elif is_seller:
        button_text = "商品編集"
        button_url =  reverse('bikeChange', args=[bike.id])  #reverse('shuppin:edit_bike', args=[bike.id])  # 編集ページへのURL

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product_type = 'bike'
            comment.product_id = bike_id
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect('shohin:shohin_bike', bike_id=bike_id)
    else:
        form = CommentForm()

    context = {
        'bike': bike,
        'images': images,
        'comments': comments,
        'form': form,
        'like_count': like_count,
        'liked': liked,
        'button_text': button_text,
        'button_url': button_url,
        'is_seller': is_seller,
    }
    return render(request, 'shohin/shohin_bike.html', context)

def shohin_car_view(request, car_id):
    car = get_object_or_404(CInfoModel, id=car_id)
    images = CImageModel.objects.filter(testcar=car)
    comments = Comment.objects.filter(product_type='car', product_id=car_id).order_by('created_at')
    
    # いいねの合計数を取得
    like_count = Like.objects.filter(product_type='car', product_id=car_id).count()
    
    # ユーザーが既にいいねしているか確認
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            product_type='car',
            product_id=car_id
        ).exists()

    # 出品者かどうかをチェック
    is_seller = request.user.is_authenticated and request.user == car.user
    
    # ボタンの状態を決定
    button_text = "購入"
    button_url = reverse('product_purchase', args=[car.class_name, car.id])
    
    # 購入後画面、商品編集画面はここにURLを！　osawa
    if car.soldflag:
        button_text = "SOLDOUT"
        purchase=car.car_product.get()
        button_url = reverse('purchase_after', args=["Purchase_car",purchase.id]) 
    elif is_seller:
        button_text = "商品編集"
        button_url = reverse('carChange', args=[car.id])  #reverse('shuppin:edit_car', args=[car.id])  # 編集ページへのURL

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product_type = 'car'
            comment.product_id = car_id
            if request.user.is_authenticated:    # この行を追加
                comment.user = request.user      # この行を追加
            comment.save()
            return redirect('shohin:shohin_car', car_id=car_id)
    else:
        form = CommentForm()

    context = {
        'car': car,
        'images': images,
        'comments': comments,
        'form': form,
        'like_count': like_count,
        'liked': liked,
        'button_text': button_text,
        'button_url': button_url,
        'is_seller': is_seller,
    }
    return render(request, 'shohin/shohin_car.html', context)

def shohin_motorBike_view(request, bike_id):
    bike = get_object_or_404(MCInfoModel, id=bike_id)
    images = MCImageModel.objects.filter(testmotorcycle=bike)
    comments = Comment.objects.filter(product_type='motorBike', product_id=bike_id).order_by('created_at')
    
    # いいねの合計数を取得
    like_count = Like.objects.filter(product_type='motorBike', product_id=bike_id).count()
    
    # ユーザーが既にいいねしているか確認
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            product_type='motorBike',
            product_id=bike_id
        ).exists()

    # 出品者かどうかをチェック
    is_seller = request.user.is_authenticated and request.user == bike.user
    
    # ボタンの状態を決定
    button_text = "購入"
    button_url = reverse('product_purchase', args=[bike.class_name, bike.id])
    
    # 購入後画面、商品編集画面はここにURLを！　osawa
    if bike.soldflag:
        button_text = "SOLDOUT"
        purchase=bike.mc_product.get()
        button_url = reverse('purchase_after', args=["Purchase_mc",purchase.id]) 
    elif is_seller:
        button_text = "商品編集"
        button_url = reverse('motorcycleChange', args=[bike.id])   #reverse('shuppin:edit_motorbike', args=[bike.id])  # 編集ページへのURL

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product_type = 'motorBike'
            comment.product_id = bike_id
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect('shohin:shohin_motorBike', bike_id=bike_id)
    else:
        form = CommentForm()

    context = {
        'bike': bike,
        'images': images,
        'comments': comments,
        'form': form,
        'like_count': like_count,
        'liked': liked,
        'button_text': button_text,
        'button_url': button_url,
        'is_seller': is_seller,
    }
    return render(request, 'shohin/shohin_motorBike.html', context)

@login_required
def like_product(request, product_type, product_id):
    # 既にいいねしているか確認
    like, created = Like.objects.get_or_create(
        user=request.user,
        product_type=product_type,
        product_id=product_id
    )

    if not created:
        # 既にいいねしている場合は削除（いいねを取り消す）
        like.delete()
        liked = False
    else:
        liked = True

    # いいねの合計数を取得
    like_count = Like.objects.filter(product_type=product_type, product_id=product_id).count()

    # JSONレスポンスを返す
    return JsonResponse({
        'liked': liked,
        'like_count': like_count,
    })

def like_status(request, product_type, product_id):
    # ユーザーが既にいいねしているか確認
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            product_type=product_type,
            product_id=product_id
        ).exists()

    # いいねの合計数を取得
    like_count = Like.objects.filter(product_type=product_type, product_id=product_id).count()

    # JSONレスポンスを返す
    return JsonResponse({
        'liked': liked,
        'like_count': like_count,
    })