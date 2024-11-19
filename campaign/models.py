from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Email(models.Model):
    address = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    last_failed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.address


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(help_text="HTML content of the newsletter")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="newsletters"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("email", "newsletter")

    def __str__(self):
        return f"{self.email.address} subscribed to {self.newsletter.title}"


class ScheduledTask(models.Model):
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, null=True, blank=True
    )
    emails = models.ManyToManyField(Email, blank=True) 
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task for {self.newsletter.title} at {self.schedule_time}"

    def save(self, *args, **kwargs):
        if self.schedule_time <= timezone.now():
            raise ValueError("Scheduled time must be in the future.")
        super().save(*args, **kwargs)
