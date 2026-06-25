import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saipem_hse.settings')
django.setup()

from hse_module.hse_safety.serializers import IncidentSerializer
from hse_module.hse_safety.models import Incident

try:
    incident = Incident.objects.get(id=1)
    serializer = IncidentSerializer(incident, data={"status": "INVESTIGATING"}, partial=True)
    if serializer.is_valid():
        serializer.save()
        print(f"Success! Status is now: {incident.status}")
    else:
        print(f"Errors: {serializer.errors}")
except Exception as e:
    print(f"Exception: {e}")
