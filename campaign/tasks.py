from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from campaign.models import Newsletter, Email, Subscriber, ScheduledTask


@shared_task
def send_newsletter(newsletter_id=None, email_ids=None):
    if newsletter_id:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        recipients = Subscriber.objects.filter(newsletter=newsletter)
        email_addresses = [subscriber.email.address for subscriber in recipients]
    elif email_ids:
        email_addresses = list(
            Email.objects.filter(id__in=email_ids).values_list("address", flat=True)
        )

    html_content = render_to_string(
        "newsletter-template.html",
        {
            "title": newsletter.title,
            "content": newsletter.message,
        },
    )

    email = EmailMultiAlternatives(
        subject=f"Newsletter: {newsletter.title}",
        body="This is an HTML email; use an HTML-compatible client.",
        from_email="your-email@example.com",
        to=[],
        bcc=email_addresses,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


@shared_task
def process_scheduled_tasks():
    tasks = ScheduledTask.objects.filter(is_processed=False, schedule_time__lte=now())
    for task in tasks:
        if task.newsletter:
            send_newsletter.delay(task.newsletter.id)
        elif task.emails.exists():
            send_newsletter.delay(
                None, email_ids=list(task.emails.values_list("id", flat=True))
            )
        task.is_processed = True
        task.save()
