from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Document

@receiver(post_save, sender=Document)
def notify_course_subscribers(sender, instance, created, **kwargs):
    """
    Send email notifications:
    1. To post author when approved/denied
    2. To course subscribers when approved
    """
    print(f"🔔 Signal triggered for post {instance.id}, status: {instance.status}")
    
    # Notify author if post is approved or rejected (not pending)
    if instance.status in ['approved', 'rejected']:
        notify_author(instance)
    
    # Only notify subscribers when approved
    if instance.status != 'approved':
        print(f"❌ Post status is '{instance.status}', not approved. Skipping subscriber notification.")
        return
    
    course = instance.course
    if not course:
        print("❌ No course associated with post. Skipping email.")
        return
    
    print(f"📚 Course: {course.name}")
    
    # Get subscribers who have notifications enabled
    subscribers = course.subscribers.filter(email_notifications=True).exclude(id=instance.user.id)
    
    print(f"👥 Found {subscribers.count()} subscribers with notifications enabled")
    
    if not subscribers.exists():
        print("❌ No subscribers to notify. Skipping email.")
        return
    
    # Prepare email context for subscribers
    post_url = f"{settings.FRONTEND_URL}/document/{instance.id}"
    
    context = {
        'course_name': course.name,
        'post_title': instance.title,
        'post_content': instance.post[:200] + '...' if len(instance.post) > 200 else instance.post,
        'author_name': instance.user.get_full_name() or instance.user.username,
        'faculty_name': course.faculty.name,
        'semester': course.semester,
        'post_url': post_url,
    }
    
    # Send email to each subscriber
    for subscriber in subscribers:
        context['user_name'] = subscriber.get_full_name() or subscriber.username
        
        html_message = render_to_string('emails/new_post_notification.html', context)
        
        try:
            send_mail(
                subject=f'Nova objava: {instance.title}',
                message=f'Nova objava u {course.name}: {instance.title}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                html_message=html_message,
                fail_silently=True,
            )
            print(f"✉️ Email sent to subscriber {subscriber.email}")
        except Exception as e:
            print(f"❌ Failed to send email to {subscriber.email}: {e}")


def notify_author(instance):
    """
    Send email to post author when their post is approved or denied.
    """
    author = instance.user
    course = instance.course
    
    if not author.email:
        print(f"❌ Author {author.username} has no email address")
        return
    
    # Check if author wants email notifications
    if not author.email_notifications:
        print(f"❌ Author {author.username} has notifications disabled")
        return
    
    post_url = f"{settings.FRONTEND_URL}/document/{instance.id}"
    moderator_name = instance.reviewed_by.get_full_name() if instance.reviewed_by else "Moderator"
    
    context = {
        'user_name': author.get_full_name() or author.username,
        'post_title': instance.title,
        'course_name': course.name if course else "Nepoznat kolegij",
        'moderator_name': moderator_name,
        'post_url': post_url,
    }
    
    if instance.status == 'approved':
        template = 'emails/post_approved_notification.html'
        subject = f'✅ Tvoja objava "{instance.title}" je odobrena!'
        print(f"📧 Sending approval email to author {author.email}")
    else:  # rejected
        template = 'emails/post_denied_notification.html'
        subject = f'❌ Tvoja objava "{instance.title}" nije odobrena'
        print(f"📧 Sending rejection email to author {author.email}")
    
    html_message = render_to_string(template, context)
    
    try:
        send_mail(
            subject=subject,
            message=f'Tvoja objava "{instance.title}" - status: {instance.status}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[author.email],
            html_message=html_message,
            fail_silently=True,
        )
        print(f"✉️ Email sent to author {author.email}")
    except Exception as e:
        print(f"❌ Failed to send email to author {author.email}: {e}")