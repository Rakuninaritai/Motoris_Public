from django.core.management.base import BaseCommand
from shuppin.models import MotorcycleModel,CarModel

# 車種ごとにバイクのデータを保存しておく
class Command(BaseCommand):
    help = "Seed MotorcycleModel data"
    
    def handle(self,*args, **kwargs):
        self.motorcycle()
        self.car()

    def motorcycle(self):
        # 既存データを削除（必要なら）
        MotorcycleModel.objects.all().delete()
        
        # データのリスト
        data = [
            #HONDA
            {"maker":"HONDA","displacement":"50cc以下","name":"Ape","type":"1"},
            {"maker":"HONDA","displacement":"50cc以下","name":"Bite","type":"1"},
            {"maker":"HONDA","displacement":"50cc以下","name":"CB50","type":"1"},
            {"maker":"HONDA","displacement":"50cc以下","name":"CRF50F","type":"1"},
            {"maker":"HONDA","displacement":"51~125cc","name":"Ape100","type":"1"},
            {"maker":"HONDA","displacement":"51~125cc","name":"C200","type":"1"},
            {"maker":"HONDA","displacement":"51~125cc","name":"C92","type":"1"},
            {"maker":"HONDA","displacement":"51~125cc","name":"CB125","type":"1"},
            {"maker":"HONDA","displacement":"126~250cc","name":"ADV150","type":"1"},
            {"maker":"HONDA","displacement":"126~250cc","name":"AX-1","type":"1"},
            {"maker":"HONDA","displacement":"126~250cc","name":"C71","type":"1"},
            {"maker":"HONDA","displacement":"126~250cc","name":"CB150R","type":"1"},
            {"maker":"HONDA","displacement":"251~400cc","name":"400X","type":"1"},
            {"maker":"HONDA","displacement":"251~400cc","name":"BROS400","type":"1"},
            {"maker":"HONDA","displacement":"251~400cc","name":"CB-1","type":"1"},
            {"maker":"HONDA","displacement":"251~400cc","name":"CB350","type":"1"},
            {"maker":"HONDA","displacement":"401~750cc","name":"BROS650","type":"1"},
            {"maker":"HONDA","displacement":"401~750cc","name":"CB400F(408cc)","type":"1"},
            {"maker":"HONDA","displacement":"401~750cc","name":"CB450","type":"1"},
            {"maker":"HONDA","displacement":"401~750cc","name":"CB500Four","type":"1"},
            {"maker":"HONDA","displacement":"751cc以上","name":"CB1000r","type":"1"},
            {"maker":"HONDA","displacement":"751cc以上","name":"CB1000Super Four","type":"1"},
            {"maker":"HONDA","displacement":"751cc以上","name":"CB1100","type":"1"},
            {"maker":"HONDA","displacement":"751cc以上","name":"CB1100EX","type":"1"},
            #Kawasaki
            {"maker":"Kawasaki","displacement":"50cc以下","name":"AR50","type":"1"},
            {"maker":"Kawasaki","displacement":"50cc以下","name":"AV50","type":"1"},
            {"maker":"Kawasaki","displacement":"50cc以下","name":"KSR-1","type":"1"},
            {"maker":"Kawasaki","displacement":"51~125cc","name":"90SS","type":"1"},
            {"maker":"Kawasaki","displacement":"51~125cc","name":"Dトラッカー125","type":"1"},
            {"maker":"Kawasaki","displacement":"51~125cc","name":"KDX125SR","type":"1"},
            {"maker":"Kawasaki","displacement":"51~125cc","name":"KLX110","type":"1"},
            {"maker":"Kawasaki","displacement":"126~250cc","name":"175TR","type":"1"},
            {"maker":"Kawasaki","displacement":"126~250cc","name":"220SS","type":"1"},
            {"maker":"Kawasaki","displacement":"126~250cc","name":"250TR","type":"1"},
            {"maker":"Kawasaki","displacement":"126~250cc","name":"BALIUS","type":"1"},
            {"maker":"Kawasaki","displacement":"251~400cc","name":"350A7","type":"1"},
            {"maker":"Kawasaki","displacement":"251~400cc","name":"350SS","type":"1"},
            {"maker":"Kawasaki","displacement":"251~400cc","name":"400SS","type":"1"},
            {"maker":"Kawasaki","displacement":"251~400cc","name":"ER-4n","type":"1"},
            {"maker":"Kawasaki","displacement":"401~750cc","name":"500SS","type":"1"},
            {"maker":"Kawasaki","displacement":"401~750cc","name":"500SSマッハⅢ","type":"1"},
            {"maker":"Kawasaki","displacement":"401~750cc","name":"750SS","type":"1"},
            {"maker":"Kawasaki","displacement":"401~750cc","name":"750ターボ","type":"1"},
            {"maker":"Kawasaki","displacement":"751cc以上","name":"1000GTR","type":"1"},
            {"maker":"Kawasaki","displacement":"751cc以上","name":"1400GTR","type":"1"},
            {"maker":"Kawasaki","displacement":"751cc以上","name":"GPZ1000RX","type":"1"},
            {"maker":"Kawasaki","displacement":"751cc以上","name":"GPZ1100","type":"1"},
            #YAMAHA
            {"maker":"YAMAHA","displacement":"50cc以下","name":"BJ","type":"1"},
            {"maker":"YAMAHA","displacement":"50cc以下","name":"BW'S","type":"1"},
            {"maker":"YAMAHA","displacement":"50cc以下","name":"DT50","type":"1"},
            {"maker":"YAMAHA","displacement":"50cc以下","name":"FT50","type":"1"},
            {"maker":"YAMAHA","displacement":"51~125cc","name":"AS-1","type":"1"},
            {"maker":"YAMAHA","displacement":"51~125cc","name":"AXIS90","type":"1"},
            {"maker":"YAMAHA","displacement":"51~125cc","name":"AXISトリート","type":"1"},
            {"maker":"YAMAHA","displacement":"51~125cc","name":"AXIS Z","type":"1"},
            {"maker":"YAMAHA","displacement":"126~250cc","name":"AEROX155","type":"1"},
            {"maker":"YAMAHA","displacement":"126~250cc","name":"AG200","type":"1"},
            {"maker":"YAMAHA","displacement":"126~250cc","name":"BRONCO","type":"1"},
            {"maker":"YAMAHA","displacement":"126~250cc","name":"CZ150R","type":"1"},
            {"maker":"YAMAHA","displacement":"251~400cc","name":"FZ400","type":"1"},
            {"maker":"YAMAHA","displacement":"251~400cc","name":"FZ400R","type":"1"},
            {"maker":"YAMAHA","displacement":"251~400cc","name":"FZR400","type":"1"},
            {"maker":"YAMAHA","displacement":"251~400cc","name":"FZR400RR","type":"1"},
            {"maker":"YAMAHA","displacement":"401~750cc","name":"FZ6 Fazer S2","type":"1"},
            {"maker":"YAMAHA","displacement":"401~750cc","name":"FZ6R","type":"1"},
            {"maker":"YAMAHA","displacement":"401~750cc","name":"FZ6-S FAZER","type":"1"},
            {"maker":"YAMAHA","displacement":"401~750cc","name":"FZ750","type":"1"},
            {"maker":"YAMAHA","displacement":"751cc以上","name":"BOLT","type":"1"},
            {"maker":"YAMAHA","displacement":"751cc以上","name":"BOLT Cスペック","type":"1"},
            {"maker":"YAMAHA","displacement":"751cc以上","name":"FAZER8","type":"1"},
            {"maker":"YAMAHA","displacement":"751cc以上","name":"FJ1200","type":"1"},
            #SUZUKI
            {"maker":"SUZUKI","displacement":"50cc以下","name":"2サイクルバーディー50","type":"1"},
            {"maker":"SUZUKI","displacement":"50cc以下","name":"4サイクルバーディー50","type":"1"},
            {"maker":"SUZUKI","displacement":"50cc以下","name":"DR-Z50","type":"1"},
            {"maker":"SUZUKI","displacement":"50cc以下","name":"GAG","type":"1"},
            {"maker":"SUZUKI","displacement":"51~125cc","name":"DR125","type":"1"},
            {"maker":"SUZUKI","displacement":"51~125cc","name":"DR-Z70","type":"1"},
            {"maker":"SUZUKI","displacement":"51~125cc","name":"EN125","type":"1"},
            {"maker":"SUZUKI","displacement":"51~125cc","name":"GN125","type":"1"},
            {"maker":"SUZUKI","displacement":"126~250cc","name":"250SB","type":"1"},
            {"maker":"SUZUKI","displacement":"126~250cc","name":"ACROSS","type":"1"},
            {"maker":"SUZUKI","displacement":"126~250cc","name":"Bandit250","type":"1"},
            {"maker":"SUZUKI","displacement":"126~250cc","name":"Bandit250LTD","type":"1"},
            {"maker":"SUZUKI","displacement":"251~400cc","name":"Bandit400","type":"1"},
            {"maker":"SUZUKI","displacement":"251~400cc","name":"Bandit400 LTD","type":"1"},
            {"maker":"SUZUKI","displacement":"251~400cc","name":"Bandit400 LTD V","type":"1"},
            {"maker":"SUZUKI","displacement":"251~400cc","name":"Bandit400 V","type":"1"},
            {"maker":"SUZUKI","displacement":"401~750cc","name":"GS425","type":"1"},
            {"maker":"SUZUKI","displacement":"401~750cc","name":"GS450","type":"1"},
            {"maker":"SUZUKI","displacement":"401~750cc","name":"GS550E","type":"1"},
            {"maker":"SUZUKI","displacement":"401~750cc","name":"GS650G","type":"1"},
            {"maker":"SUZUKI","displacement":"751cc以上","name":"Bandit1200","type":"1"},
            {"maker":"SUZUKI","displacement":"751cc以上","name":"Bandit1200S","type":"1"},
            {"maker":"SUZUKI","displacement":"751cc以上","name":"Bandit1250F","type":"1"},
            {"maker":"SUZUKI","displacement":"751cc以上","name":"Bandit1250S","type":"1"},
        ]

        # データを作成
        # for entry in data:
        #     MotorcycleModel.objects.create(
        #         maker=entry["maker"],
        #         displacement=entry["displacement"],
        #         name=entry["name"],
        #         type=entry["type"]
        #     )

        for index, entry in enumerate(data, start=1):
            MotorcycleModel.objects.create(
                maker=entry["maker"],
                displacement=entry["displacement"],
                name=entry["name"],
                type=entry["type"],
                number=index,  # 一意の番号を割り当て
            )

        self.stdout.write(self.style.SUCCESS("MotorcycleModel data seeded successfully!"))
    
    def car(self):
        CarModel.objects.all().delete()
        
        data = [
            {"maker":"TOYOTA","name":"プリウス","type":"1"},
            {"maker":"TOYOTA","name":"アルファード","type":"1"},
            {"maker":"TOYOTA","name":"クラウン","type":"1"},
            {"maker":"TOYOTA","name":"ハイエース","type":"1"},
            {"maker":"HONDA","name":"N-BOX","type":"1"},
            {"maker":"HONDA","name":"シビック","type":"1"},
            {"maker":"HONDA","name":"フィット","type":"1"},
            {"maker":"HONDA","name":"フリード","type":"1"},
            {"maker":"NISSAN","name":"スカイライン","type":"1"},
            {"maker":"NISSAN","name":"セレナ","type":"1"},
            {"maker":"NISSAN","name":"フェアレディZ","type":"1"},
            {"maker":"NISSAN","name":"エクストレイル","type":"1"},
        ]
        
        # for entry in data:
        #     CarModel.objects.create(
        #         maker=entry["maker"],
        #         name=entry["name"],
        #         type=entry["type"]
        #     )
            
        for index, entry in enumerate(data, start=1):
            CarModel.objects.create(
                maker=entry["maker"],
                name=entry["name"],
                type=entry["type"],
                number=index,  # 一意の番号を割り当て
            )

        self.stdout.write(self.style.SUCCESS("CarModel data seeded successfully!"))
            