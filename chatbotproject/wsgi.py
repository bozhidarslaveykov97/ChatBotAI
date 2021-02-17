"""
WSGI config for chatbotproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
import logging
from django.core.wsgi import get_wsgi_application

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/ChatBotAI/")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbotproject.settings')

application = get_wsgi_application()