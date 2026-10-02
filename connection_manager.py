from typing import Dict,Set
from fastapi import WebSocket



class ConnectionManager:
    def __init__(self):
        self.user_socket:Dict[int,WebSocket] ={}
        self.admin_sockets: Set[WebSocket] = set()

 
    async def connect_user(self,user_id:int,websocket: WebSocket):
        await websocket.accept()
        self.user_socket[user_id] = websocket
    async def connect_admin(self,websocket: WebSocket):
        await websocket.accept()
        self.admin_sockets.add(websocket) 

    def disconnect_user(self,user_id:int):
        try:
            numeric_id = int(user_id)
            if numeric_id in self.user_socket:
                self.user_socket.pop(numeric_id)
        except ValueError:
            pass
        if str(user_id) in self.user_socket:
            self.user_socket.pop(str(user_id))


    async def disconnect_admin(self,websocket:WebSocket):
        self.admin_sockets.discard(websocket)

    async def send_personal_message(self,message:Dict, recipient_id:str)-> bool:
        recipient_key = int(recipient_id)
        if recipient_key in self.user_socket:
            await self.user_socket[recipient_key].send_json(message)
            return True
        return False
    async def broadcast_to_admins(self,payload:dict):
        for ws in list(self.admin_sockets):
            try:
                await ws.send_json(payload)
            except Exception:
                self.admin_sockets.discard(ws)
manager = ConnectionManager()