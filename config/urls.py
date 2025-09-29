"""
URL configuration for Motoris project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from accounts.views import register,Pwwsr,LoginView,LogoutView
from profiles.views import ProfileView, ProfileUpdateView, OtherProfileView
from top.views import topView
from events.views import EventListView, EventCreateView, EventDetailView, EnterEventView, event_entry_list_json, cancel_entry,DeleteCommentView
from events.views import EventListView, EventDetailView, EnterEventView, event_entry_list_json, cancel_entry, eventuploadfunc, event_check, event_submit, EventEntryListView

from shindan.views import shindanView,afterboughtView
from shuppin.views import befourshuppinHtmlView,motorcycleView,bcheck,submit_bike,ccheck,submit_car,submit_motorcycle,motorcycleuploadfunc,mcheck,caruploadfunc,bikeuploadfunc,shuppinHtmlView,load_MCmodelnames,load_Cmodelnames,car_edit,mc_edit,by_edit,car_delete,mc_delete,by_delete
from shohin.views import like_product, like_status

from searches.views import searchView
from purchase.views import PurchaseView,Purchase_clearView,Purchase_afterview
from formpage.views import FormView,FormAdminView,send_mail_form,send_reply

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('register/',register,name="register"),
    
    # ソーシャルログイン関連
    # ソーシャルログインで必要のないallauthのリンクはaccounts.urlsで404にする
    path('accounts/', include('accounts.urls')), 
    # 404を潜り抜けたページが404
    path('accounts/', include('allauth.urls')),  # AllauthのURLをインクルード

    
    #djangoデフォルトのlogin,logoutview
    path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    # パスワード忘れ
    path('pwwsr/',Pwwsr.as_view(), name='pwwsr'),
    
    # profiles
    path('profile/',ProfileView.as_view(),name="profile"),
    path('profile/edit/',ProfileUpdateView.as_view(),name='profile_edit'),
    path('profile/<str:user_id>/',OtherProfileView.as_view(),name='other_profile'),
    # top
    path('', topView.as_view(), name="top"),

    # events 
    path('event/post/', eventuploadfunc, name='event_post'),
    path('event/check/', event_check, name='event_check'),
    path('event/submit/', event_submit, name='event_submit'),
    path('event/list/', EventListView.as_view(), name="event_list"),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
     # entry
    path('event/<int:event_id>/event-entry/', EnterEventView.as_view(), name='enter_event'),
    path('event/<int:event_id>/entries/', event_entry_list_json, name='event_entry_list_json'), 
    path('event/<int:event_id>/cancel-entry/', cancel_entry, name='cancel_entry'),
    path('comment/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    path('event/entries/', EventEntryListView.as_view(), name='event_entries'),
    

    # markets 商品の詳細ページ
    path('shohin/', include('shohin.urls')),
     # 購入
    path('product/<str:products>/<int:product_id>/purchase/', PurchaseView.as_view(), name='product_purchase'),
     # 購入完了
    path('purchase/<str:purchase>/<int:purchase_id>/clear/', Purchase_clearView.as_view(), name='purchase_clear'),
     # 購入後
    path('purchase/<str:purchase>/<int:purchase_id>/after/', Purchase_afterview.as_view(), name='purchase_after'),

    #shindan
    path('shindan/', shindanView.as_view(), name='shindan'),
    path('shindanb/', afterboughtView.as_view(), name='afterbought'),
    #shuppin
    path('shuppin/',befourshuppinHtmlView.as_view(),name='befourshuppin'),
    path('motercycle/',motorcycleuploadfunc,name='motercycle'),
    path('mcheck/',mcheck,name='mcheck'),
    path('car/',caruploadfunc,name='car'),
    path('ccheck/',ccheck,name='ccheck'),    
    path('bike/',bikeuploadfunc,name='bike'),
    path('bcheck/',bcheck,name='bcheck'),    
    path('load-MCmodelnames/', load_MCmodelnames, name='load_MCmodelnames'),
    path('load-Cmodelnames/', load_Cmodelnames, name='load_Cmodelnames'),
    path('submit_motorcycle/', submit_motorcycle, name='submit_motorcycle'),
    path('submit_car/', submit_car, name='submit_car'),
    path('submit_bike/', submit_bike, name='submit_bike'),
    # shuppin編集
    path('motorcycleChange/<int:pk>/',mc_edit,name='motorcycleChange'),
    path('carChange/<int:pk>/',car_edit,name='carChange'),
    path('bikeChange/<int:pk>/',by_edit,name='bikeChange'),
    # 削除用の URL
    path('motorcycleChange/delete/<int:pk>/', mc_delete, name='mc_delete'),
    path('carChange/delete/<int:pk>/', car_delete, name='car_delete'),
    path('bikeChange/delete/<int:pk>/', by_delete, name='by_delete'),
     # いいね
    path('like/<str:product_type>/<int:product_id>/', like_product, name='like_product'),
    
    path('search/<str:kensaku>', searchView.as_view(), name='search'),
    
    # formpage    
    path('formpage/', FormView.as_view(), name='formpage'),
    path('formadmin/', FormAdminView.as_view(), name='formadmin'),
    path('formadmin/send_mail_form/<int:contact_id>/', send_mail_form, name='send_mail_form'),
    path('formadmin/send_reply/<int:contact_id>/', send_reply, name='send_reply'),

    # 試し用のpath
    path('tameshi/', shuppinHtmlView.as_view(), name='tameshi'),
    

]

# debugTrue時画像とstaticを配信しましょうという指示(staticは自動追加のはずだがうまくいかないので明示)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()  # DEBUG=True時のみ静的ファイルをurlpatternsに追加