import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class IncidentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("incidents_updates", self.channel_name)
        await self.accept()
        await self.send_recent_incidents()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("incidents_updates", self.channel_name)

    async def incident_created(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'incident_created',
            'message': message
        }))

    async def incident_status_changed(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'incident_status_changed',
            'message': message
        }))

    async def system_status_changed(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'system_status_changed',
            'message': message
        }))

    @database_sync_to_async
    def get_recent_incidents(self):
        from .models import Incident
        from ..hse_pob.models import WorkLocation

        incidents = Incident.objects.all().order_by('-created_at')[:5]
        result = []
        for incident in incidents:
            location_name = incident.location.deck_name if incident.location else "Unknown"

            result.append({
                'incident_id': incident.incident_id,
                'severity': incident.severity,
                'status': incident.status,
                'location': location_name,
                'description': incident.description,
                'reported_by': incident.reported_by,
                'employee_name': incident.employee_name,
                'incident_date': incident.incident_date.isoformat(),
                'created_at': incident.created_at.isoformat()
            })
        return result

    async def send_recent_incidents(self):
        incidents = await self.get_recent_incidents()
        for incident in incidents:
            await self.send(text_data=json.dumps({
                'type': 'incident_recent',
                'message': incident
            }))
