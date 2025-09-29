from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, TemplateView, ListView
from events.models import EventPost, EventEntry
from itertools import chain
from purchase.models import Purchase_car,Purchase_mc,Purchase_by
from shuppin.models import  MCInfoModel,MCImageModel,CInfoModel,CImageModel,BInfoModel,BImageModel
from shohin.models import Like

from profiles.forms import ProfileForm
# Create your views here.

User = get_user_model()

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profiles/profile.html'
    model = CInfoModel
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        car_listings = CInfoModel.objects.filter(user=self.request.user)
        mc_listings = MCInfoModel.objects.filter(user=self.request.user)
        b_listings = BInfoModel.objects.filter(user=self.request.user)
        car_purchases = Purchase_car.objects.filter(user=self.request.user).select_related('product')
        mc_purchases = Purchase_mc.objects.filter(user=self.request.user).select_related('product')
        b_purchases = Purchase_by.objects.filter(user=self.request.user).select_related('product')
        event_posts = EventPost.objects.filter(user=self.request.user).order_by('-created_at')
        event_entries = EventEntry.objects.filter(user=self.request.user).select_related('event').order_by('-created_at')



        #=========================
        # 購入、いいねした商品を取得
        #=========================
        my_purchases = []
        for purchase in car_purchases:
            product = purchase.product
            product.model_name = 'CInfoModel'
            product.action_type = 'purchase'
            product.created_at = purchase.created_at
            my_purchases.append(product)

        for purchase in mc_purchases:
            product = purchase.product
            product.model_name = 'MCInfoModel'
            product.action_type = 'purchase'
            product.created_at = purchase.created_at
            my_purchases.append(product)

        for purchase in b_purchases:
            product = purchase.product
            product.model_name = 'BInfoModel'
            product.action_type = 'purchase'
            product.created_at = purchase.created_at
            my_purchases.append(product)
            
        my_likes  = []
        for like in Like.objects.filter(user=self.request.user):
            if like.product_type == 'car':
                try:
                    product = CInfoModel.objects.get(id=like.product_id)
                    product.model_name = 'CInfoModel'
                    product.created_at = like.created_at
                    product.action_type = 'like'
                    my_likes .append(product)
                except CInfoModel.DoesNotExist:
                    continue
            elif like.product_type == 'motorBike':
                try:
                    product = MCInfoModel.objects.get(id=like.product_id)
                    product.model_name = 'MCInfoModel'
                    product.created_at = like.created_at
                    product.action_type = 'like'
                    my_likes .append(product)
                except MCInfoModel.DoesNotExist:
                    continue
            elif like.product_type == 'bike':
                try:
                    product = BInfoModel.objects.get(id=like.product_id)
                    product.model_name = 'BInfoModel'
                    product.created_at = like.created_at
                    product.action_type = 'like'
                    my_likes .append(product)
                except BInfoModel.DoesNotExist:
                    continue
                
                
        # 新着情報作成
        for post in car_listings:
            post.model_name = 'CInfoModel'
            post.action_type = 'post'
        for post in mc_listings:
            post.model_name = 'MCInfoModel'
            post.action_type = 'post'
        for post in b_listings:
            post.model_name = 'BInfoModel'
            post.action_type = 'post'
        for post in event_posts:
            post.model_name = 'EventPost'
        for entry in event_entries:
            entry.model_name = 'EventEntry'

        context['timeline'] = sorted(
            chain(car_listings, mc_listings, b_listings, event_posts, event_entries, my_likes , my_purchases),
            key=lambda x: x.created_at,
            reverse=True
        )

        # 出品購入　個別表示
        context['my_listings'] = list(chain(car_listings, mc_listings, b_listings))
        context['my_purchases'] = my_purchases
        context['my_likes'] = my_likes 
        context['target_user'] = None

        return context

class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profiles/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
    

    
class OtherProfileView(LoginRequiredMixin, ListView):
    template_name = 'profiles/profile.html'
    model = CInfoModel
    
    # ログインしているユーザーがother_profile入ってきた場合はプロフィールに飛ばす
    def get(self, request, *args, **kwargs):
        # URLからユーザーIDを取得
        user_id = self.kwargs.get('user_id')
        target_user = get_object_or_404(User, id=user_id)
        # ログインしているユーザーとurlのユーザーが同一ならリダイレクト
        if(request.user==target_user):
            return redirect('profile')
        # 条件を満たすなら普通に処理を継続する
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # URLからユーザーIDを取得
        user_id = self.kwargs.get('user_id')
        target_user = get_object_or_404(User, id=user_id)

        car_listings = CInfoModel.objects.filter(user=target_user)
        mc_listings = MCInfoModel.objects.filter(user=target_user)
        b_listings = BInfoModel.objects.filter(user=target_user)
        car_purchases = Purchase_car.objects.filter(user=target_user).select_related('product')
        mc_purchases = Purchase_mc.objects.filter(user=target_user).select_related('product')
        b_purchases = Purchase_by.objects.filter(user=target_user).select_related('product')
        event_posts = EventPost.objects.filter(user=target_user).order_by('-created_at')
        event_entries = EventEntry.objects.filter(user=target_user).select_related('event').order_by('-created_at')



        #=========================
        # 購入、いいねした商品を取得
        #=========================
        my_purchases = []
        for purchase in car_purchases:
            product = purchase.product
            product.model_name = 'CInfoModel'
            product.action_type = 'purchase'
            product.created_at = purchase.created_at
            my_purchases.append(product)

        for purchase in mc_purchases:
            product = purchase.product
            product.model_name = 'MCInfoModel'
            product.action_type = 'purchase'
            product.created_at = purchase.created_at
            my_purchases.append(product)

        for purchase in b_purchases:
            product = purchase.product
            product.model_name = 'BInfoModel'
            product.action_type = 'purchase'
            product.created_at = purchase.created_at
            my_purchases.append(product)
            
        my_likes  = []
        for like in Like.objects.filter(user=self.request.user):
            if like.product_type == 'car':
                try:
                    product = CInfoModel.objects.get(id=like.product_id)
                    product.model_name = 'CInfoModel'
                    product.created_at = like.created_at
                    product.action_type = 'like'
                    my_likes .append(product)
                except CInfoModel.DoesNotExist:
                    continue
            elif like.product_type == 'motorBike':
                try:
                    product = MCInfoModel.objects.get(id=like.product_id)
                    product.model_name = 'MCInfoModel'
                    product.created_at = like.created_at
                    product.action_type = 'like'
                    my_likes .append(product)
                except MCInfoModel.DoesNotExist:
                    continue
            elif like.product_type == 'bike':
                try:
                    product = BInfoModel.objects.get(id=like.product_id)
                    product.model_name = 'BInfoModel'
                    product.created_at = like.created_at
                    product.action_type = 'like'
                    my_likes .append(product)
                except BInfoModel.DoesNotExist:
                    continue
                
                
        # 新着情報作成
        for post in car_listings:
            post.model_name = 'CInfoModel'
            post.action_type = 'post'
        for post in mc_listings:
            post.model_name = 'MCInfoModel'
            post.action_type = 'post'
        for post in b_listings:
            post.model_name = 'BInfoModel'
            post.action_type = 'post'
        for post in event_posts:
            post.model_name = 'EventPost'
        for entry in event_entries:
            entry.model_name = 'EventEntry'

        context['timeline'] = sorted(
            chain(car_listings, mc_listings, b_listings, event_posts, event_entries, my_likes , my_purchases),
            key=lambda x: x.created_at,
            reverse=True
        )

        # 出品購入　個別表示
        context['my_listings'] = list(chain(car_listings, mc_listings, b_listings))
        context['my_purchases'] = my_purchases
        context['my_likes'] = my_likes 
        
        context['target_user'] = target_user 

        return context