from rest_framework import serializers

from apps.publication.models import Publication


class CreatePublicationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    create_by = serializers.CharField(read_only=True)
    create_at = serializers.CharField(read_only=True)

    class Meta:
        model = Publication
        fields = (
            'title', 'description', 'create_by', 'create_at',
        )
    
    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user') if 'logged_user' in kwargs else None

        super().__init__(*args, **kwargs)
    
    def create(self, validated_data) -> Publication:
        if self.logged_user:
            return Publication.objects.create(
                **validated_data, create_by_id=self.logged_user.id)
        return Publication.objects.create(**validated_data)

class ListPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = (
            'title', 'description', 'create_at', 'create_by',
        )