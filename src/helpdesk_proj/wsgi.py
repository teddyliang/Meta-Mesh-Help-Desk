"""
WSGI config for helpdesk_proj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import logging
from FAQManager.faqmanager import FAQManager
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk_proj.settings')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
)

FAQManager.start_scheduler()

application = get_wsgi_application()
