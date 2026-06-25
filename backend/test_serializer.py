import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saipem_hse.settings')
django.setup()

from hse_module.hse_safety.serializers import IncidentReportSerializer
from django.utils import timezone

data = {
    'severity': 'NEAR_MISS',
    'location': 1,
    'description': 'Test incident description from shell',
    'reported_by': 'EMP-001',
    'incident_date': timezone.now().isoformat(),
    'vessel_id': 'VES-001'
}

serializer = IncidentReportSerializer(data=data, context={'user_id': 'admin'})
if serializer.is_valid():
    try:
        incident = serializer.save()
        print(f"Success! Incident created with ID: {incident.id}")
    except Exception as e:
        print(f"Exception during save: {e}")
else:
    print(f"Serializer errors: {serializer.errors}")
