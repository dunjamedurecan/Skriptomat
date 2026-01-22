from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Document
import threading


def send_email_in_background(subject, message, from_email, recipient_list, html_message):
    """
    Helper function to send email in a separate thread (non-blocking).
    """
    import time
    print(f"🔄 Starting email send to {recipient_list}...")
    print(f"   Subject: {subject}")
    print(f"   From: {from_email}")
    print(f"   Thread ID: {threading.current_thread().ident}")
    start_time = time.time()
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,  # Show errors in logs temporarily
        )
        elapsed = time.time() - start_time
        print(f"✉️ Email successfully sent to {recipient_list} in {elapsed:.2f}s")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Failed to send email to {recipient_list} after {elapsed:.2f}s")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        import traceback
        print(f"   Traceback:\n{traceback.format_exc()}")

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
        
        # Send email in background thread (non-blocking)
        email_thread = threading.Thread(
            target=send_email_in_background,
            args=(
                f'Nova objava: {instance.title}',
                f'Nova objava u {course.name}: {instance.title}',
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                html_message,
            )
        )
        email_thread.daemon = True
        email_thread.start()
        print(f"📧 Email sending started in background for {subscriber.email}")


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
    
    # Send email in background thread (non-blocking)
    email_thread = threading.Thread(
        target=send_email_in_background,
        args=(
            subject,
            f'Tvoja objava "{instance.title}" - status: {instance.status}',
            settings.DEFAULT_FROM_EMAIL,
            [author.email],
            html_message,
        )
    )
    email_thread.daemon = True
    email_thread.start()
    print(f"📧 Email sending started in background for author {author.email}")