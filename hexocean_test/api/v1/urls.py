from django.urls import path
from rest_framework import routers

from hexocean_test.api.v1.views import ImageViewSet, image_download


router = routers.SimpleRouter()
router.register(r'image', ImageViewSet)
urlpatterns = router.urls + [
    path('image_download/', image_download)
]