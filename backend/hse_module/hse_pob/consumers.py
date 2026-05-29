import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class POBConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Gabung ke grup "pob_dashboard"
        await self.channel_layer.group_add("pob_dashboard", self.channel_name)
        await self.accept()

        # Send recent POB logs (last 5) to newly connected client
        await self.send_recent_logs()

    async def disconnect(self, close_code):
        # Keluar dari grup
        await self.channel_layer.group_discard("pob_dashboard", self.channel_name)

    # Fungsi untuk mengirim pesan ke Vue.js
    async def send_location_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Fungsi untuk mengirim emergency alert
    async def send_emergency_alert(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'emergency_alert',
            'message': message
        }))

    @database_sync_to_async
    def get_recent_logs(self):
        from .models import POBLog
        from ..hse_ptw.models import Employee

        logs = POBLog.objects.all().order_by('-timestamp')[:5]
        result = []
        for log in logs:
            try:
                employee = Employee.objects.get(emp_id=log.emp_id)
                employee_name = employee.full_name
            except Employee.DoesNotExist:
                employee_name = log.emp_id

            result.append({
                'action': log.action,
                'employee_name': employee_name,
                'location': log.deck_location,
                'timestamp': log.timestamp.isoformat()
            })
        return result

    async def send_recent_logs(self):
        logs = await self.get_recent_logs()
        for log in logs:
            await self.send(text_data=json.dumps({
                'message': log
            }))