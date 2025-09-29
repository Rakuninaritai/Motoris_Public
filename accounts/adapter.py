# ソーシャルアカウントログイン用アダプタ(重複排除するためにカスタムアダプタ作成)
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_app(self, request, provider, client_id=None):
        # provider と settings.SITE_ID に基づいて SocialApp を取得、重複除去のため distinct() を使用
        qs = SocialApp.objects.filter(provider=provider, sites__id=settings.SITE_ID).distinct()
        try:
            return qs.get()
        except SocialApp.DoesNotExist:
            raise Exception("No SocialApp configured for provider '{0}'".format(provider))
