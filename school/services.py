from celery import shared_task
from django.core.mail import send_mail
import config.settings as settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_mailing(user_emails, course_title):
    subject = f"Обновление курса: {course_title}"
    message = f"Материалы курса {course_title} были обновлены!"

    from_email = settings.EMAIL_HOST_USER

    for email in user_emails:
        try:
            send_mail(subject, message, from_email, [email], fail_silently=False,)
            logger.info(f"Уведомление отправлено на адрес электронной почты: {email}")
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление на адрес электронной почты: {email}: {e}")
