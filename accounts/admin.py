from django.contrib import admin

# Register your models here.
# formはユーザーモデルを取得してして使用することが出来る(modelはdjangoが立ち上がる上がる前から読み込まないといけないから取得できない)
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
admin.site.register(CustomUser)