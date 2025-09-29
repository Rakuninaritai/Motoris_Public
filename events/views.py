import os
import uuid
import json
import shutil
import base64
from datetime import datetime
from itertools import groupby
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Prefetch
from django import forms
from django.views import View
from django.views.generic import FormView
from .models import EventPost, Comment, EventEntry, UploadImageModel, UploadImageModel
from .forms import EventPostForm, EventImageForm, EventSearchForm, CommentForm
from django.views.generic import ListView,CreateView,DetailView

# Create your views here
class EventListView(ListView):
    model = EventPost
    queryset = EventPost.objects.prefetch_related('images')
    template_name = 'events/event_list.html'
    context_object_name = 'event_posts'

    def get_queryset(self):
        queryset = EventPost.objects.prefetch_related(
            Prefetch('images', queryset=UploadImageModel.objects.all())
        )
        form = EventSearchForm(self.request.GET)

        if form.is_valid():
            region = form.cleaned_data.get('region')
            year_month = form.cleaned_data.get('year_month')
            if region:
                region_to_prefectures = {
                    '北海道地方': ['北海道'],
                    '東北地方': ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'],
                    '関東地方': ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県'],
                    '北陸地方': ['新潟県', '富山県', '石川県', '福井県'],
                    '中部地方': ['山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
                    '近畿地方': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
                    '中国地方': ['鳥取県', '島根県', '岡山県', '広島県', '山口県'],
                    '四国地方': ['徳島県', '香川県', '愛媛県', '高知県'],
                    '九州地方': ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県'],
                    '沖縄地方': ['沖縄県'],
                }
                
                if region in region_to_prefectures:
                    prefectures = region_to_prefectures.get(region, [])
                    queryset = queryset.filter(prefecture_field__in=prefectures)
                else:
                    queryset = queryset.filter(prefecture_field=region)

            if year_month:
                year, month = map(int, year_month.split('-'))
                queryset = queryset.filter(
                    Q(event_date__year=year) & Q(event_date__month=month)
                )

        # event_dateで降順に並べ替え
        queryset = queryset.order_by('-event_date')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventSearchForm(self.request.GET)  # 検索フォームをコンテキストに追加
        return context
    
class EventCreateView(LoginRequiredMixin, CreateView):
    model = EventPost
    form_class = EventPostForm
    template_name = 'events/event_create.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        images = self.request.FILES.getlist('images')
        for image in images:
            UploadImageModel.objects.create(event_post=self.object, image=image)

        return super().form_valid(form)

def eventuploadfunc(request):
    if request.method == 'POST':
        event_form = EventPostForm(request.POST)
        
        if event_form.is_valid():
            request.session['event_form_data'] = request.POST
            image_data = []
            
            # 複数ファイル処理
            files = request.FILES.getlist('image')
            for file in files:
                encoded_image = base64.b64encode(file.read()).decode('utf-8')
                image_data.append(f"data:{file.content_type};base64,{encoded_image}")
            
            request.session['event_image_data'] = image_data
            return redirect('event_check')
    else:
        event_form = EventPostForm()
    
    context = {
        'event_form': event_form,
    }
    return render(request, 'events/event_post.html', context)

def event_submit(request):
    if request.method == 'POST':
        form_data = request.session.get('event_form_data', {})
        image_data = request.session.get('event_image_data', [])
        event_form = EventPostForm(form_data)
        
        if event_form.is_valid():
            event_instance = event_form.save(commit=False)
            event_instance.user = request.user
            event_instance.save()
            
            # 複数画像の保存
            for image_base64 in image_data:
                content = ContentFile(base64.b64decode(image_base64.split(',')[1]))
                image_model = UploadImageModel(event_post=event_instance)
                image_model.image.save(f"event_{event_instance.id}_{datetime.now().timestamp()}.jpg", content)
            
            # セッションデータの削除
            del request.session['event_form_data']
            del request.session['event_image_data']
            return redirect('event_list')
        
    return redirect('event_check')

def event_check(request):
    session_form = request.session.get('event_form_data', {})
    images = request.session.get('event_image_data', [])
    
    context = {
        'event_form': EventPostForm(session_form),
        'images': images,
    }
    return render(request, 'events/event_check.html', context)
            
            
            

class EventDetailView(DetailView):
    model = EventPost
    template_name = 'events/event_detail.html'
    context_object_name = 'event_post'
    
    # コメント
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        # 現在のユーザーがイベントに参加しているかをチェック
        if self.request.user.is_authenticated:
            is_entry = EventEntry.objects.filter(event=self.object, user=self.request.user).exists()  # 参加予定をチェック
        else:
            is_entry = False  # 未認証の場合は参加していないとみなす

        context['is_entry'] = is_entry

        # イベント投稿者の情報を追加
        event_post = self.get_object()
        user = event_post.user  # イベント投稿者のユーザーオブジェクト
        
        context['event_user'] = user
        context['event_user_profile_image'] = user.profile.get_image_url()  # ユーザーのアイコンURL
        context['event_user_name'] = user.username

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            
            if request.user.is_authenticated:
                comment.user = request.user
                comment.save()
                return redirect('event_detail', pk=self.object.pk)
            else:
                return redirect('login')
            
        return self.render_to_response(self.get_context_data(comment_form=form))


#参加予定
class EnterEventView(View):
    def post(self, request, event_id):
        event = get_object_or_404(EventPost, id=event_id)
        EventEntry.objects.get_or_create(user=request.user, event=event)
        
        return redirect('event_detail', pk=event_id)
    
def event_entry_list_json(request, event_id):
    event_entries = EventEntry.objects.filter(event_id=event_id).select_related('user', 'user__profile')
    
    entries_data = []
    for entry in event_entries:
        entry_data = {
            'username': entry.user.username,
            'user_id': entry.user.id,  # ユーザーIDを追加（プロフィールページへのリンク用）
            'bio': entry.user.profile.bio if hasattr(entry.user, 'profile') and entry.user.profile.bio else "",
        }
        
        # プロフィール画像URLを追加
        if hasattr(entry.user, 'profile') and hasattr(entry.user.profile, 'get_image_url'):
            try:
                entry_data['profile_image_url'] = entry.user.profile.get_image_url()
            except:
                # エラーが発生した場合は画像URLを含めない
                pass
        
        entries_data.append(entry_data)
    
    data = {'entries': entries_data}
    return JsonResponse(data)


def cancel_entry(request, event_id):
    if request.method == 'POST':
        user = request.user
        try:
            event = EventPost.objects.get(id=event_id)

            if user.is_authenticated:
                entry = EventEntry.objects.filter(event=event, user=user).first()
                if entry:
                    entry.delete()
                    return JsonResponse({
                        'success': True, 
                        'message': 'イベント参加をキャンセルしました。'
                    })
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': '参加予定が見つかりません。'
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'ログインが必要です。'
                }, status=401)

        except EventPost.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'イベントが見つかりません。'
            }, status=404)

    return JsonResponse({
        'success': False, 
        'message': '無効なリクエスト。'
    }, status=405)

class EventEntryListView(LoginRequiredMixin, ListView):
    """ログインユーザーが参加予定のイベント一覧を表示するビュー"""
    model = EventPost
    template_name = 'events/event_entries.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        # ユーザーが参加登録したイベントを取得
        return EventPost.objects.filter(
            evententry__user=self.request.user
        ).prefetch_related('images').order_by('event_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '参加予定のイベント'
        return context

class DeleteCommentView(View):
    def post(self,request,comment_id,*args,**kwargs):
        comment=get_object_or_404(Comment,id=comment_id)
        if comment.user != request.user:
            return HttpResponseForbidden("このコメントを削除する権限がありません。")

        # コメント削除
        comment.delete()
        return redirect('event_detail', pk=comment.post.id)