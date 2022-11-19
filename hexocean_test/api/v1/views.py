import mimetypes
import os
from datetime import timedelta

from PIL import Image
from django.http import HttpResponse
from django.utils import timezone
from django.utils.encoding import smart_str
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from request_token.decorators import use_request_token
from rest_framework.response import Response

from request_token.models import RequestToken

from hexocean_test.api.v1.serializers import ImageListSerializer, ImageUploadSerializer, GetDownloadLinkSerializer
from hexocean_test.web.models import Image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ImageListSerializer
        else:
            return ImageUploadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        instance.delete()

    @action(detail=True, methods=['post'])
    def get_download_link(self, request, pk=None):
        if self.request.user.tier.expiring_link_access:
            image = self.get_object()
            serializer = GetDownloadLinkSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = RequestToken.objects.create_token(
                scope="image",
                data={
                    'image_id': image.id
                },
                expiration_time=timezone.now() + timedelta(seconds=serializer.data['exp'])
            )
            return Response({'link': request.build_absolute_uri(f'/api/v1/image_download?rt={token.jwt()}')})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


@use_request_token(scope='image')
@api_view()
def image_download(request):
    if request.token:
        image_id = (
            request.token.data['image_id']
            if hasattr(request, 'token')
            else None
        )
        obj = Image.objects.filter(id=image_id).first()
        if obj:
            image = obj.file
            content_type = mimetypes.guess_type(image.path)
            response = HttpResponse(image.open('rb'), content_type=content_type)
            response['X-Sendfile'] = image.path
            response['Content-Length'] = image.size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(image.name)
            return response
        else:
            return Response({'detail': 'No image with this id.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Token bad or expired.'}, status=status.HTTP_403_FORBIDDEN)