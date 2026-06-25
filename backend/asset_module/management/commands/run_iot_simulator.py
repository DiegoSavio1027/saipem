import time
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from asset_module.models import Asset, MachineryEquipment, TelemetryLog

class Command(BaseCommand):
    help = 'Runs the virtual IoT simulator to generate persistent telemetry data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting Virtual IoT Simulator..."))
        
        while True:
            try:
                # Update Machinery
                machinery = MachineryEquipment.objects.all()
                for mac in machinery:
                    if mac.needs_maintenance:
                        # High vibration when needs maintenance
                        vibration_change = random.uniform(0.0, 0.15)
                        temp_change = random.uniform(0.0, 0.8)
                        new_vib = float(mac.current_vibration) + vibration_change
                        new_temp = float(mac.current_temperature) + temp_change
                    else:
                        new_vib = random.uniform(1.2, 3.8)
                        new_temp = random.uniform(42.0, 68.5)

                    new_vib = min(max(new_vib, 1.0), 12.0)
                    new_temp = min(max(new_temp, 30.0), 150.0)

                    mac.current_vibration = round(new_vib, 2)
                    mac.current_temperature = round(new_temp, 2)
                    mac.save(update_fields=['current_vibration', 'current_temperature'])

                    TelemetryLog.objects.create(
                        machinery=mac,
                        vibration=mac.current_vibration,
                        temperature=mac.current_temperature
                    )

                self.stdout.write(self.style.SUCCESS(f"[{timezone.now()}] IoT Telemetry synchronized."))
                
                # Wait 5 seconds before next update to simulate real-time stream
                time.sleep(5)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in IoT simulator: {e}"))
                time.sleep(5)
