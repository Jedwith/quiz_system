from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, FastAPI
from typing import Dict, Tuple, Optional
from src.schemas.websocket import UserInfo, TestData, SessionInfo
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # room_code (str) -> {user_id (int): (WebSocket, WSUserInfo)}
        self.active_connections: Dict[str, Dict[int, Tuple[WebSocket, UserInfo]]] = {}
        # room_code (str) -> session_info
        self.session_data: Dict[str, SessionInfo] = {}

    async def connect(self, websocket: WebSocket, room_code: str, user: UserInfo):
        await websocket.accept()
        if room_code not in self.active_connections:
            self.active_connections[room_code] = {}

        # self.active_connections.setdefault(room_code, {})[user.id] = (websocket, user)
        self.active_connections[room_code][user.id] = (websocket, user)
        logger.info(f"User {user.id} connected to room {room_code}")

    async def disconnect(self, room_code: str, user_id: int):
        if room_code not in self.active_connections or user_id not in self.active_connections[room_code]:
            return

        ws, user = self.active_connections[room_code].pop(user_id)
        logger.info(f"User {user.id} disconnected from room {room_code}")

        try:
            await ws.close(code=1000)
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

        if not self.active_connections[room_code]:
            del self.active_connections[room_code]
            if room_code in self.session_data:
                del self.session_data[room_code]

    async def broadcast(self, room_code: str, message: dict, exclude: Optional[int] = None):
        room = self.active_connections.get(room_code)
        if not room:
            return

        for ws, user in room.values():
            if exclude is not None and user.id not in exclude:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user.id}: {e}")

    async def broadcast_to_role(self, room_code: str, role: str, message: dict):
        room = self.active_connections.get(room_code)
        if not room:
            return

        for ws, user in room.values():
            if user.role == role:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user.id}: {e}")

    async def send_personal(self, room_code: str, user_id: int, message: dict):
        room = self.active_connections.get(room_code)
        if not room:
            return

        connection = room.get(user_id)
        if not connection:
            return

        ws, user = connection
        try:
            await ws.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message to user {user.id}: {e}")

    async def start_session(self, room_code: str, session_id: int, test_id: int, test_data: TestData):
        questions = test_data.questions
        session_info = SessionInfo(
            session_id=session_id,
            test_id=test_id,
            status="active",
            started_at=datetime.now().isoformat(),
            test_name=test_data.test_name,
            test_description=test_data.test_description,
            total_questions=len(questions),
            questions=questions
        )

        self.session_data[room_code] = session_info

        logger.info(f"Session {session_id} started in room {room_code} with {len(questions)} questions")

        await self.broadcast(room_code, {
            "type": "session_started",
            "data": session_info.model_dump(mode='json')
        })

    async def end_session(self, room_code: str):
        session_info = self.session_data.get(room_code)
        if not session_info:
            logger.warning(f"No active session found in room {room_code}")
            return

        session_info.status = "finished"
        session_info.ended_at = datetime.now().isoformat()

        self.session_data[room_code] = session_info

        logger.info(f"Session {session_info.session_id} ended in room {room_code}")

        await self.broadcast(room_code, {
            "type": "session_finished",
            "data": session_info.model_dump(mode='json')
        })

        del self.session_data[room_code]

    def get_connected_users(self, room_code: str):
        room = self.active_connections.get(room_code)
        if not room:
            return []

        users = [user for _, user in room.values()]

        return users







