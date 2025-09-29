from django.core.management.commands.runserver import Command as RunserverCommand
from shuppin.models import MotorcycleModel
from django.core.management import call_command


class Command(RunserverCommand):
    def handle(self, *args, **options):
        # サーバー起動時にデバッグメッセージを出力
        # このカスタムが読み込まれていたらメッセージ
        print("Custom runserver is being executed!")
        
        # dbにレコードが存在していたらtrueの否定(存在していなければ実行)(毎回実行するとinfoの商品名リセットされる)
        if not MotorcycleModel.objects.exists():
            try:
                # seed_motorcycle_modelsコマンドの実行
                print("Executing seed_motorcycle_models...")
                call_command('seed_motorcycle_models')
                print("Data seeding completed successfully!")
            except Exception as e:
                # エラー発生時のメッセージ
                print(f"Error during data seeding: {e}")
            
            
        # try:
        #     # collectstatic コマンドの実行
        #     print("Executing collectstatic...")
        #     # コマンド実行,詳細非表示,対話モードオフ(確認取らない),消して上書き
        #     call_command('collectstatic', verbosity=0, interactive=False,clear=True)
        #     print("Static files collected successfully!")
        # except Exception as e:
        #     print(f"Error during collectstatic: {e}")

        # 元のrunserverの挙動を継続
        super().handle(*args, **options)