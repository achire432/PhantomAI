"""
DATA SERVICE
=============
Purpose:
- Export user data
- Import user data
- Preserve conversations, messages, notes, tasks, and memories

Important:
All imported data is attached to the authenticated user.
Existing data is not overwritten.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.models.conversation import Conversation
from backend.app.models.message import Message
from backend.app.models.note import Note
from backend.app.models.task import Task
from backend.app.models.memory import Memory

from backend.app.schemas.message import MessageCreate
from backend.app.schemas.note import NoteCreate
from backend.app.schemas.task import TaskCreate
from backend.app.schemas.memory import MemoryCreate

from backend.app.services.conversation import (
    create_conversation,
    add_message,
)
from backend.app.services.notes_service import create_note
from backend.app.services.tasks_service import create_task
from backend.app.services.memory_service import store_memory


def export_user_data(
    db: Session,
    user_id: int
) -> dict:
    """
    Export all data belonging to one user.

    Includes:
    - Conversations
    - Messages
    - Notes
    - Tasks
    - Memories
    """

    # Get only this user's conversations
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )

    conversations_data = []

    for conversation in conversations:

        messages = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation.id
            )
            .order_by(Message.created_at.asc())
            .all()
        )

        conversations_data.append({
            "id": conversation.id,
            "title": conversation.title,
            "created_at": (
                conversation.created_at.isoformat()
                if conversation.created_at
                else None
            ),
            "updated_at": (
                conversation.updated_at.isoformat()
                if conversation.updated_at
                else None
            ),
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                    "created_at": (
                        message.created_at.isoformat()
                        if message.created_at
                        else None
                    )
                }
                for message in messages
            ]
        })

    # Notes
    notes = (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .all()
    )

    notes_data = [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": (
                note.created_at.isoformat()
                if note.created_at
                else None
            ),
            "updated_at": (
                note.updated_at.isoformat()
                if note.updated_at
                else None
            )
        }
        for note in notes
    ]

    # Tasks
    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .all()
    )

    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
            "created_at": (
                task.created_at.isoformat()
                if task.created_at
                else None
            ),
            "updated_at": (
                task.updated_at.isoformat()
                if task.updated_at
                else None
            )
        }
        for task in tasks
    ]

    # Memories
    memories = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .all()
    )

    memories_data = [
        {
            "key": memory.key,
            "value": memory.value,
            "category": memory.category,
            "importance": memory.importance,
            "created_at": (
                memory.created_at.isoformat()
                if memory.created_at
                else None
            )
        }
        for memory in memories
    ]

    return {
        "user_id": user_id,
        "exported_at": datetime.utcnow().isoformat(),
        "conversations": conversations_data,
        "notes": notes_data,
        "tasks": tasks_data,
        "memories": memories_data
    }


def import_user_data(
    db: Session,
    user_id: int,
    data: dict
) -> dict:
    """
    Import user data.

    Existing records are not overwritten.
    Imported records are added to the authenticated user's account.
    """

    imported_count = {
        "conversations": 0,
        "messages": 0,
        "notes": 0,
        "tasks": 0,
        "memories": 0
    }

    # ---------------------------------------------------------
    # Verify user
    # ---------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise ValueError("User not found.")

    # ---------------------------------------------------------
    # Import conversations
    # ---------------------------------------------------------

    for conversation_data in data.get(
        "conversations",
        []
    ):

        title = conversation_data.get(
            "title",
            "Conversation"
        )

        conversation = create_conversation(
            db,
            user,
            f"Imported: {title}"
        )

        imported_count["conversations"] += 1

        # Import messages
        for message_data in conversation_data.get(
            "messages",
            []
        ):

            role = message_data.get("role")
            content = message_data.get("content")

            if not role or content is None:
                continue

            message = MessageCreate(
                role=role,
                content=content
            )

            add_message(
                db,
                conversation,
                message
            )

            imported_count["messages"] += 1

    # ---------------------------------------------------------
    # Import notes
    # ---------------------------------------------------------

    for note_data in data.get(
        "notes",
        []
    ):

        title = note_data.get(
            "title",
            "Imported Note"
        )

        content = note_data.get(
            "content",
            ""
        )

        note = NoteCreate(
            title=title,
            content=content
        )

        create_note(
            db,
            user_id,
            note
        )

        imported_count["notes"] += 1

    # ---------------------------------------------------------
    # Import tasks
    # ---------------------------------------------------------

    for task_data in data.get(
        "tasks",
        []
    ):

        task = TaskCreate(
            title=task_data.get(
                "title",
                "Imported Task"
            ),
            description=task_data.get(
                "description"
            ),
            priority=task_data.get(
                "priority",
                "medium"
            ),
            due_date=(
                datetime.fromisoformat(
                    task_data["due_date"]
                )
                if task_data.get("due_date")
                else None
            )
        )

        create_task(
            db,
            user_id,
            task
        )

        imported_count["tasks"] += 1

    # ---------------------------------------------------------
    # Import memories
    # ---------------------------------------------------------

    for memory_data in data.get(
        "memories",
        []
    ):

        memory = MemoryCreate(
            key=memory_data["key"],
            value=memory_data["value"],
            category=memory_data.get(
                "category",
                "general"
            ),
            importance=memory_data.get(
                "importance",
                3
            )
        )

        store_memory(
            db,
            user_id,
            memory
        )

        imported_count["memories"] += 1

    return imported_count
