from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
   
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password", "profile_image", "cover_image")
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
   
    
class LoginSerializer(serializers.Serializer):
    login_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        login_id = data.get("login_id")
        password = data.get("password")
        
        user = None
        if "@" in login_id:
            user = authenticate(email=login_id, password=password)
        else:
            user = authenticate(username=login_id, password=password)
        if not user:
            raise serializers.ValidationError("Invalid login ceredntials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data["user"] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
   
    profile_image = serializers.ImageField(required=False, allow_null=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    

    class Meta:
        model = User
        fields = ("id", "username", "email",  "profile_image", "cover_image")
        read_only_fields = ("id", "email")
        
    

        
    
        
    