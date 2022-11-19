from rest_framework import serializers

from hexocean_test.web.models import Image
from sorl.thumbnail import get_thumbnail

class ImageListSerializer(serializers.ModelSerializer):

    thumbnails = serializers.SerializerMethodField()

    def get_thumbnails(self, obj):
        request = self.context.get('request')
        user = request.user
        thumbnails = []
        image = obj.file
        for height in user.tier.thumbnail_sizes:
            width = int(image.width * height / image.height)
            thumbnail = get_thumbnail(image.file, f'{width}x{height}', crop='center', quality=99).url
            thumbnails.append({str(height): request.build_absolute_uri(thumbnail)})
        return thumbnails

    def __init__(self, *args, **kwargs):

        if  not kwargs['context'].get('request').user.tier.original_photo_access:
            del self.fields['file']

        super().__init__(*args, **kwargs)


    class Meta:
        model = Image
        fields = ['id', 'file', 'thumbnails']

class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['file']


class GetDownloadLinkSerializer(serializers.Serializer):

    exp = serializers.IntegerField(min_value=300, max_value=3000, required=True)
