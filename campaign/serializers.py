from rest_framework import serializers
from django.contrib.auth.models import User
from campaign.models import Email, Newsletter, ScheduledTask, Subscriber

class ScheduledTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTask
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        return attrs


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["id", "address", "is_active"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "title", "message", "created_by"]


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["id", "email", "newsletter"]


class AnonymousSubscriptionSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    newsletter_id = serializers.IntegerField()

    def validate(self, data):
        try:
            Newsletter.objects.get(id=data["newsletter_id"])
        except Newsletter.DoesNotExist:
            raise serializers.ValidationError("Newsletter not found.")
        return data

    def create(self, validated_data):
        email, created = Email.objects.get_or_create(
            address=validated_data["email_address"], defaults={"is_active": True}
        )
        newsletter = Newsletter.objects.get(id=validated_data["newsletter_id"])
        Subscriber.objects.get_or_create(email=email, newsletter=newsletter)
        return {"email": email.address, "newsletter": newsletter.title}
