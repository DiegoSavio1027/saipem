import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class PTWConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("ptw_updates", self.channel_name)
        await self.accept()
        await self.send_recent_ptws()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ptw_updates", self.channel_name)

    async def ptw_created(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'ptw_created',
            'message': message
        }))

    async def ptw_status_changed(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'ptw_status_changed',
            'message': message
        }))

    @database_sync_to_async
    def get_recent_ptws(self):
        from .models import PermitToWork
        from hr_module.models import Employee

        ptws = PermitToWork.objects.all().order_by('-created_at')[:5]
        result = []
        for ptw in ptws:
            try:
                employee = Employee.objects.get(emp_id=ptw.emp_id)
                employee_name = employee.full_name
            except Employee.DoesNotExist:
                employee_name = ptw.emp_id

            result.append({
                'permit_id': ptw.permit_id,
                'emp_id': ptw.emp_id,
                'employee_name': employee_name,
                'permit_type': ptw.permit_type,
                'status': ptw.status,
                'deck_location': ptw.deck_location.id if ptw.deck_location else None,
                'deck_location_name': ptw.deck_location.deck_name if ptw.deck_location else None,
                'created_at': ptw.created_at.isoformat(),
                'approved_by': ptw.approved_by,
                'approved_at': ptw.approved_at.isoformat() if ptw.approved_at else None
            })
        return result

    async def send_recent_ptws(self):
        ptws = await self.get_recent_ptws()
        for ptw in ptws:
            await self.send(text_data=json.dumps({
                'type': 'ptw_recent',
                'message': ptw
            }))
