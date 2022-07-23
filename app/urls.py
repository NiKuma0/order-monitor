from rest_framework.routers import DefaultRouter

from app.views import OrderViewSet

order_router = DefaultRouter()
order_router.register(r'orders', OrderViewSet)


urlpatterns = order_router.urls
