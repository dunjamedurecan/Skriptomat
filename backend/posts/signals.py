from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Document

@receiver(post_save, sender=Document)
def notify_course_subscribers(sender, instance, created, **kwargs):
    """
    Send email notifications to subscribers when a post is approved.
    Only sends on approval, not on creation.
    """
    print(f"🔔 Signal triggered for post {instance.id}, status: {instance.status}")
    
    # Only notify when status changes to approved (not on initial creation)
    if instance.status != 'approved':
        print(f"❌ Post status is '{instance.status}', not approved. Skipping email.")
        return
    
    # Get the course and its subscribers
    course = instance.course
    if not course:
        return
    
    print(f"📚 Course: {course.name}")
    
    # Get subscribers who have notifications enabled
    subscribers = course.subscribers.filter(email_notifications=True).exclude(id=instance.user.id)
    
    print(f"👥 Found {subscribers.count()} subscribers with notifications enabled")
    
    if not subscribers.exists():
        print("❌ No subscribers to notify. Skipping email.")
        return
    
    # Prepare email context
    post_url = f"{settings.FRONTEND_URL}/document/{instance.id}"  # You'll need to add FRONTEND_URL to settings
    
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
                message=f'Nova objava u {course.name}: {instance.title}',  # Plain text fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                html_message=html_message,
                fail_silently=False,  # Show errors during development
            )
            print(f"✉️ Email sent to {subscriber.email}")
        except Exception as e:
            print(f"❌ Failed to send email to {subscriber.email}: {e}")