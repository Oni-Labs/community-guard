from rest_framework import serializers

from apps.account.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'confirm_password',
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password = validated_data.get('password')
        confirm_password = validated_data.pop('confirm_password')

        if confirm_password != password:
            raise serializers.ValidationError({
                'confirm_password': ['passwords do not match']
            })
    
        return validated_data

    def create(self, validated_data) -> User | serializers.ValidationError:
        try:
            user = User(**validated_data)
            user.set_password(validated_data.get('password'))
            user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError(str(e)) 


# class ListUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'username', 'email', 'is_active', 'is_superuser'
#         )