from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    index,
    EmailListView,
    NewsletterView,
    ScheduleMailView,
    RegisterView,
    SubscribeNewsletterView,
    AnonymousSubscribeNewsletterView,
    ScheduledTaskListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("emails/", EmailListView.as_view(), name="email-list"),
    path("newsletters/", NewsletterView.as_view(), name="newsletter-list"),
    path("subscribe/", SubscribeNewsletterView.as_view(), name="subscribe-newsletter"),
    path(
        "subscribe/anonymous/",
        AnonymousSubscribeNewsletterView.as_view(),
        name="anonymous-subscribe",
    ),
    path("schedule/", ScheduleMailView.as_view(), name="schedule-mail"),
    path("tasks/", ScheduledTaskListView.as_view(), name="scheduled-task-list"),
]
