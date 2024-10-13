from rest_framework import serializers

from apps.publication.models import Publication


class CreatePublicationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Publication
        fields = (
            'title', 'description',
        )