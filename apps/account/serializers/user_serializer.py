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
        email = validated_data.get('email')
        username = validated_data.get('username')

        fields_errors = dict()

        if confirm_password != password:
            fields_errors['confirm_password'] = 'passwords do not match'
    
        if User.objects.filter(
            email=email
        ).exists():
            fields_errors['email'] = 'email already registered'
        
        if User.objects.filter(
            username=username
        ).exists():
            fields_errors['username'] = 'username already registered'
        
        if fields_errors:
            raise serializers.ValidationError(fields_errors)
    
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