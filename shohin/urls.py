from django.urls import path
from .views import shohin_bike_view, shohin_car_view, shohin_motorBike_view
from .views import like_product, like_status

app_name = 'shohin'
urlpatterns = [
    path('bike/<int:bike_id>/', shohin_bike_view, name='shohin_bike'),
    path('car/<int:car_id>/', shohin_car_view, name='shohin_car'),
    path('motorBike/<int:bike_id>/', shohin_motorBike_view, name='shohin_motorBike'),
    path('like/<str:product_type>/<int:product_id>/', like_product, name='like_product'),
    path('like-status/<str:product_type>/<int:product_id>/', like_status, name='like_status'),
]
