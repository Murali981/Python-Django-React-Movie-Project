from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet, RatingViewSet, UserViewSet

# We have to register our ViewSets in the below router
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('movies', MovieViewSet)  # This movie string will be just inside our path below.
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
