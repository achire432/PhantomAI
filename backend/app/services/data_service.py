"""
DATA SERVICE
=============
Purpose: Export and import user data.

Why This Matters:
- Backup your conversations
- Migration to new system
- Safety net before major changes

How It Works:
1. Exports all user data as JSON
2. Can be imported back later
3. Supports conversations, notes, tasks, memory
"""

import json
from sqlalchemy.orm import Session
from backend.app.models.conversation import Conversation
from backend.app.models.message import Message
from backend.app.models.note import Note
from backend.app.models.task import Task
from backend.app.models.memory import Memory
from datetime import datetime

def export_user_data(db: Session, user_id: int) -> dict:
    """
    Export all user data as JSON.
    
    Returns:
    {
        "user_id": 2,
        "exported_at": "2026-08-04T10:00:00",
        "conversations": [...],
        "notes": [...],
        "tasks": [...],
        "memories": [...]
    }
    """
    
    # Get conversations
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).all()
    
    conv_data = []
    for conv in conversations:
        messages = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).all()
        conv_data.append({
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "messages": [{
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            } for msg in messages]
        })
    
    # Get notes
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    notes_data = [{
        "id": n.id,
        "title": n.title,
        "content": n.content,
        "created_at": n.created_at.isoformat(),
        "updated_at": n.updated_at.isoformat()
    } for n in notes]
    
    # Get tasks
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    tasks_data = [{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "priority": t.priority,
        "status": t.status,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat()
    } for t in tasks]
    
    # Get memories
    memories = db.query(Memory).filter(Memory.user_id == user_id).all()
    memories_data = [{
        "key": m.key,
        "value": m.value,
        "category": m.category,
        "importance": m.importance,
        "created_at": m.created_at.isoformat()
    } for m in memories]
    
    return {
        "user_id": user_id,
        "exported_at": datetime.utcnow().isoformat(),
        "conversations": conv_data,
        "notes": notes_data,
        "tasks": tasks_data,
        "memories": memories_data
    }

def import_user_data(db: Session, user_id: int, data: dict) -> dict:
    """
    Import user data from JSON.
    
    Warning: This will merge data, not overwrite.
    """
    imported_count = {
        "conversations": 0,
        "notes": 0,
        "tasks": 0,
        "memories": 0
    }
    
    # Import conversations
    for conv_data in data.get("conversations", []):
        # Skip if already exists? We'll create new ones
        from backend.app.services.conversation import create_conversation, add_message
        from backend.app.schemas.message import MessageCreate
        from backend.app.models.user import User
        
        user = db.query(User).filter(User.id == user_id).first()
        
        conv = create_conversation(db, user, f"Imported: {conv_data.get('title', 'Conversation')}")
        
        for msg in conv_data.get("messages", []):
            message = MessageCreate(role=msg["role"], content=msg["content"])
            add_message(db, conv.id, message)
        
        imported_count["conversations"] += 1
    
    # Import notes
    for note_data in data.get("notes", []):
        from backend.app.services.tools.notes import create_note
        from backend.app.schemas.note import NoteCreate
        
        note = NoteCreate(
            title=note_data["title"],
            content=note_data["content"]
        )
        create_note(db, user_id, note)
        imported_count["notes"] += 1
    
    # Import tasks
    for task_data in data.get("tasks", []):
        from backend.app.services.tools.tasks import create_task
        from backend.app.schemas.task import TaskCreate
        
        task = TaskCreate(
            title=task_data["title"],
            description=task_data.get("description"),
            priority=task_data.get("priority", "medium"),
            due_date=datetime.fromisoformat(task_data["due_date"]) if task_data.get("due_date") else None
        )
        create_task(db, user_id, task)
        imported_count["tasks"] += 1
    
    # Import memories
    for mem_data in data.get("memories", []):
        from backend.app.services.memory_service import store_memory
        from backend.app.schemas.memory import MemoryCreate
        
        mem = MemoryCreate(
            key=mem_data["key"],
            value=mem_data["value"],
            category=mem_data.get("category", "general"),
            importance=mem_data.get("importance", 3)
        )
        store_memory(db, user_id, mem)
        imported_count["memories"] += 1
    
    return imported_count