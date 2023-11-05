from django.core.mail import send_mail
from celery_demo.main import cel
from django.conf import settings
import logging
logger = logging.getLogger('django')
@cel.task(name='celery_demo.email.tasks.send_mail_link')
def send_mail_link(to_email, verify_url):
    """
    发送验证邮箱邮件
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    """
    subject = "多多商城邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用多多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject, "", settings.EMAIL_HOST_USER, [to_email], html_message=html_message)
    except Exception as e:
        logger.error(e)
