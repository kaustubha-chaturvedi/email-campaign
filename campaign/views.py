from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from campaign.models import Email, Newsletter, Subscriber, ScheduledTask
from campaign.serializers import (
    AnonymousSubscriptionSerializer,
    EmailSerializer,
    NewsletterSerializer,
    ScheduledTaskSerializer,
    UserSerializer,
)
from campaign.tasks import send_newsletter

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class EmailListView(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class NewsletterView(generics.ListCreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class SubscribeNewsletterView(APIView):
    def post(self, request):
        email_id = request.data.get("email_id")
        newsletter_id = request.data.get("newsletter_id")

        try:
            email = Email.objects.get(id=email_id)
            newsletter = Newsletter.objects.get(id=newsletter_id)
            Subscriber.objects.create(email=email, newsletter=newsletter)
            return Response(
                {"message": "Subscribed successfully!"}, status=status.HTTP_201_CREATED
            )
        except Email.DoesNotExist:
            return Response(
                {"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Newsletter.DoesNotExist:
            return Response(
                {"error": "Newsletter not found."}, status=status.HTTP_404_NOT_FOUND
            )


class AnonymousSubscribeNewsletterView(APIView):
    def post(self, request):
        serializer = AnonymousSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                {"message": f"Subscribed {result['email']} to {result['newsletter']}!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleMailView(APIView):
    def post(self, request):
        serializer = ScheduledTaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            if task.newsletter:
                send_newsletter.delay(task.newsletter.id)
            elif task.emails.exists():
                send_newsletter.delay(
                    None, email_ids=list(task.emails.values_list("id", flat=True))
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduledTaskListView(generics.ListAPIView):
    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def index(request):
    return Response({"message": "Welcome to Campaign API!"})