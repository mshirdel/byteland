from celery.decorators import task
from celery.utils.log import get_task_logger

from .utils import send_activation_email
from .models import User

logger = get_task_logger(__name__)


@task(name='send_activation_email_task')
def send_activation_email_task(user_id, use_https, site_name, site_domain):
    logger.info("Send activation email")
    return send_activation_email(user_id, use_https, site_name, site_domain)
