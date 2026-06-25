import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saipem_hse.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Get admin user
user = User.objects.filter(is_superuser=True).first()
if not user:
    print("No superuser found!")
    exit(1)

client = Client()
client.force_login(user)

response = client.patch('/api/v1/hse/incidents/1/', {'status': 'INVESTIGATING'}, content_type='application/json')
print(f"Status Code: {response.status_code}")
print(f"Response: {response.content.decode('utf-8')}")
