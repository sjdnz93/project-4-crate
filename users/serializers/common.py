from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation, hashers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    
    def validate(self, data):
        print('VALIDATE DATA =>', data)

        password = data.pop('password')
        print('PASSWORD', password)

        password_confirmation = data.pop('password_confirmation')
        print('PASSWORD_CONF', password_confirmation)

        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        
        password_validation.validate_password(password)

        data['password'] = hashers.make_password(password)

        print('DATA POST CUSTOM VALIDATION => ', data)

        return data


    class Meta:
        model = User
        fields = '__all__'

class UserCollection(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('collection',)      

class UserWishlist(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('wishlist',)  

class UserFollowing(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('following',)    

class UserInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_image', 'favourite_album', 'favourite_genre', 'id', 'collection',)

class Username(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')        