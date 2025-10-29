from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from accounts.models import Profile


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(request=self.context.get("request"), username=username, password=password)

            if not user:
                raise serializers.ValidationError(
                    {"detail": "Unable to log in with provided credentials."
                     }, code="authorization"
                )
        else:
            raise serializers.ValidationError({
                "detail": "Must include username and password."
            }, code="authorization")

        attrs["user"] = user
        return attrs




class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."}
            )
        return attrs

    def create(self, validated_data):
        """Create and return a new user"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    avatar = serializers.ImageField(source='profile.avatar', required=False)
    bio = serializers.CharField(source='profile.bio', required=False, allow_blank=True)
    preferences = serializers.JSONField(source='profile.preferences', required=False)
    timezone = serializers.CharField(source='profile.timezone', required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'bio', 'preferences', 'timezone'
        )
        read_only_fields = ('id', 'username',)

    def update(self, instance, validated_data):
        """
        Optimize DB operations by updating the related Profile in a single save.
        """
        profile_data = validated_data.pop('profile', {})
        user_updated = False
        profile_updated = False

        # Update User fields
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                user_updated = True

        # Update Profile fields
        profile = getattr(instance, 'profile', None)
        if not profile:
            # Handle edge case: if profile not auto-created
            profile = Profile.objects.create(user=instance)

        for attr, value in profile_data.items():
            if getattr(profile, attr) != value:
                setattr(profile, attr, value)
                profile_updated = True

        # Save only if changed
        if user_updated:
            instance.save(update_fields=list(validated_data.keys()))
        if profile_updated:
            profile.save(update_fields=list(profile_data.keys()))

        return instance

