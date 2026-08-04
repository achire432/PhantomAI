from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.schemas.auth import UserLogin, TokenResponse
from backend.app.schemas.conversation import ConversationCreate, ConversationResponse
from backend.app.schemas.message import MessageCreate, MessageResponse
from backend.app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from backend.app.schemas.task import TaskCreate, TaskUpdate, TaskResponse 
from backend.app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse 
from backend.app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from backend.app.schemas.context import ContextUpdate, ContextResponse
from backend.app.schemas.memory import MemoryCreate, MemoryUpdate, MemoryResponse