from django.contrib import admin
from django.urls import path, include

from livros.views import ReviewsViewSet, UserViewSet, WishListViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'wish_list', WishListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('livros.urls')),
    path('', include(router.urls)),
]
