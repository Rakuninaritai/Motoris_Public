from django.contrib import admin
# Register your models here.
#消えたdb motorcycleshuppin,motorcycleImage,carshuppin,carImage,bikeshuppin,bikeImage 書き換えshuto

# from .models import motorcycleshuppin,motorcycleImage
from .models import MCImageModel,MCInfoModel,MotorcycleModel,CImageModel,CInfoModel,CarModel,BImageModel,BInfoModel
# # Register your models here.
# admin.site.register(motorcycleshuppin)
# admin.site.register(motorcycleImage)
admin.site.register(MCImageModel)
admin.site.register(MCInfoModel)
admin.site.register(MotorcycleModel)
admin.site.register(CImageModel)
admin.site.register(CInfoModel)
admin.site.register(CarModel)
admin.site.register(BImageModel)
admin.site.register(BInfoModel)
